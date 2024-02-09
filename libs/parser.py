import copy
import glob
from io import StringIO

import jmespath
import pandas as pd
import textfsm


def st_parser(st):
    st.title("Parser")

    log_text = ""
    template = ""
    parser_template = ""
    parsed_list = list()
    template_root_dir = "files/templates/"
    template_dir_full_path = glob.glob(f"{template_root_dir}*.textfsm")
    template_dir = list(map(lambda x: x.replace(template_root_dir,""),template_dir_full_path))

    log_block, parser_block = st.columns(2)

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
            parser_template = st.text_area("テンプレート", template, height=391)

    st.divider()
    if log_text and parser_template:
        fsm = textfsm.TextFSM(template)
        header = fsm.header
        parsed_data = fsm.ParseText(text)

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