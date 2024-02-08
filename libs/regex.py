
import re 

def st_regex(st):
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
