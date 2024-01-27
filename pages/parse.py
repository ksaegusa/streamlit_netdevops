import copy
import glob
from io import StringIO

import jmespath
import pandas as pd
import streamlit as st
import textfsm

st.set_page_config(layout="wide")
st.title("Parser")

parsed_list = list()
template_root_dir = "files/templates/"
template_dir_full_path = glob.glob(f"{template_root_dir}*.textfsm")
template_dir = list(map(lambda x: x.replace(template_root_dir,""),template_dir_full_path))

log_upload = st.toggle("ログアップロード")
if log_upload:
    log_file = st.file_uploader("ログファイル")
else:
    log_file = st.text_area("テキスト貼り付け")

template_upload = st.toggle("テンプレートアップロード")
if template_upload:
    parser_file = st.file_uploader("パーサー")
else:
    parser_file = st.selectbox("パーサー", template_dir)

if log_file and parser_file:
    if log_upload:
        text = log_file.getvalue().decode("utf-8")
    else:
        text = log_file
    if template_upload:
        template = StringIO(parser_file.getvalue().decode("utf-8"))
    else:
        with open(template_root_dir + parser_file, "r", encoding="UTF-8") as f:
            template = StringIO(f.read())
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