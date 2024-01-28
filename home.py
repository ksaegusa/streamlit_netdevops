
import re 
import copy
import glob
from io import StringIO

import jmespath
import pandas as pd
import streamlit as st
import textfsm
from netmiko import ConnectHandler

st.title("NetDevOpsSupporter")
parser, regex, commander = st.tabs(["Parser", "Regex","Commander"])

with parser:
    st.title("Parser")

    parsed_list = list()
    template_root_dir = "files/templates/"
    template_dir_full_path = glob.glob(f"{template_root_dir}*.textfsm")
    template_dir = list(map(lambda x: x.replace(template_root_dir,""),template_dir_full_path))

    log_upload = st.toggle("ログアップロード")
    if log_upload:
        log_file = st.file_uploader("ログファイル")
    else:
        log_file = st.text_area("テキスト貼り付け", key="parser_textarea")

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

with regex:
    st.title("Regex")

    re_log_file = ""
    re_log_upload = st.toggle("ログアップデート")

    if re_log_upload:
        re_log_file = st.file_uploader("ログアップロード")
    else:
        re_text = st.text_area("テキスト貼り付け", key="res_textarea")

    if re_log_file:
        re_text = re_log_file.getvalue().decode("utf-8")
        container = st.container(border=True, height=400)
        container.code(re_text, language="log")

    regex_string = st.text_input("正規表現", "\s+")
    if st.button("抽出"):
        lines = re_text.splitlines()
        res_lines = list()
        for line in lines:
            if re.match(rf"{regex_string}", line):
                res_lines.append(line)
        st.write(f"Condition: {regex_string}")
        st.write(f"Result   : Hit {len(res_lines)} lines")
        res_container = st.container(border=True, height=250)
        res_container.code("\n".join(res_lines), language="log")

with commander:
    st.title("Commander")
    # NOTE: 適当にピックアップ
    #       Netmikoのプラットフォーム対応は下記を参照
    #       https://ktbyers.github.io/netmiko/PLATFORMS.html
    device_type_list =[
        "cisco_ios",
        "cisco_asa",
        "cisco_nxos",
        "cisco_xe",
        "cisco_xr",
        "linux",
        "vyos",
        "yamaha",
    ]

    with st.expander("認証情報"):
        address = st.text_input("アドレス","X.X.X.X")
        user = st.text_input("ユーザー","admin")
        password = st.text_input("パスワード", "password")
        secret = st.text_input("enableパスワード", "")
        device_type = st.selectbox("デバイスタイプ", device_type_list)

    command = st.text_input("コマンド","show ip route")

    device = {
        "device_type": device_type,
        "host": address,
        "username": user,
        "password": password,
        "secret": secret
    }

    if st.button("実行"):
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command(command)

        if secret:
            net_connect.enable()

        commander_container = st.container(border=True, height=700)
        commander_container.code(output, language="log")
        st.download_button(
            label="テキストダウンロード",
            data=output,
            file_name=f"{address}_{command.replace(' ','_').replace('|','_')}.text"
        )
