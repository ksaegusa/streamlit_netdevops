import copy
import glob
from io import StringIO

import jmespath
import pandas as pd
import textfsm

from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_prompt():
    template = """
    ステップ1: コンテキストと質問から主要なフィルター条件を特定。
    ステップ2: JSONデータの構造を確認し、フィルターに必要な属性を決定。
    ステップ3: JSONデータの構造を確認し、フィルターに必要なメソッドを決定。
    ステップ4: 対象属性の値が数値の際は``で値を囲んでください、数値でない場合は''で囲ってください。
    ステップ5: JMESPathクエリを形成し、条件に基づいてデータを抽出。

    下記URLでクエリ方法を確認してください
    https://jmespath.org/tutorial.html

    キーを数値として扱う場合は、to_numberを利用してください
    値が含まれることの確認は、containsを利用してください
    値が検索文字列から始まっているかどうかの確認は、starts_withを利用してください
    値が検索文字列で終わるかどうかの確認は、ends_withを利用してください

    クエリ文のみ回答してください

    - コンテキストここから -------------------------
    {context}
    -----------------------------------------------
    {question}
    """
    prompt_template = PromptTemplate(
        input_variables=["context", "question"], # {adjective}と{content}を変数とします
        template=template, 
        )
    return prompt_template

def exec_gpt(prompt_template, question,context, api_key):
    model = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0,)
    chain = prompt_template | model | StrOutputParser()
    res = chain.invoke({'context': context, 'question':question})
    print(res)
    return res

def st_parser(st):
    st.title("Parser")

    log_text = ""
    template = ""
    parsed_list = list()
    template_root_dir = "files/templates/"
    template_dir_full_path = glob.glob(f"{template_root_dir}*.textfsm")
    template_dir = list(map(lambda x: x.replace(template_root_dir,""),template_dir_full_path))
    parsed_list = []
    log_block, parser_block = st.columns(2)

    if "api_key" not in st.session_state:
        st.session_state.api_key = ''

    with log_block:
        log_upload = st.toggle("ログアップロード")
        if log_upload:
            log_file = st.file_uploader("ログファイル")
            if log_file:
                text = log_file.getvalue().decode("utf-8")
                log_text = st.text_area("ログ", text, height=391)
        else:
            log_file = st.text_area("テキスト貼り付け", key="parser_textarea")
            log_text = log_file

    with parser_block:
        template_upload = st.toggle("テンプレートアップロード")
        if template_upload:
            parser_file = st.file_uploader("パーサー")
            if parser_file:
                template = parser_file.getvalue().decode("utf-8")
        else:
            parser_file = st.selectbox("パーサー", template_dir)
            if parser_file:
                with open(template_root_dir + parser_file, "r", encoding="utf-8") as f:
                    template = f.read()
        if template:
            template = st.text_area("テンプレート", template, height=391)

    st.divider()
    if log_text and template:
        fsm = textfsm.TextFSM(StringIO(template))
        header = fsm.header
        parsed_data = fsm.ParseText(log_text)

        for i in parsed_data:
            obj = {}
            for n,m in zip(i,header):
                obj[m] = n
            parsed_list.append(obj)

        df = pd.DataFrame(parsed_list)
        st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic"
        )
    else:
        st.write("ファイルがありません")

    query  =st.text_input("クエリ文", "[?PROTOCOL == `C`]")
    if st.button("クエリ実行"):
        query_list = copy.deepcopy(parsed_list)
        queried_list = jmespath.search(query, query_list)
        queried_df = pd.DataFrame(queried_list)
        st.write(queried_df)

    if parsed_list:
        st.divider()
        st.subheader("AIにクエリ文を聞く")
        with st.popover("API Key Setting"):
            st.session_state.api_key = st.text_input("OpenAI API Key")
        if st.session_state.api_key:
            question = st.text_input("確認内容を質問")
            if st.button("実行",key='ask_llm'):
                prompt_template = generate_prompt()
                context = parsed_list
                with st.chat_message('AI'):
                    st.code(exec_gpt(prompt_template,question,context,st.session_state.api_key),language='log')
        else:
            st.write("API Keyを設定してください")
