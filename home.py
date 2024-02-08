
import streamlit as st

from libs.parser import st_parser
from libs.regex import st_regex
from libs.commander import st_commander

st.set_page_config(page_title="NetDevOpsSupporter", layout="wide")
st.title("NetDevOpsSupporter")
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

parser, regex, commander = st.tabs(["Parser", "Regex","Commander"])

with parser:
    st_parser(st)

with regex:
    st_regex(st)

with commander:
    st_commander(st)
