
import streamlit as st

from libs.parser import st_parser
from libs.regex import st_regex
from libs.commander import st_commander

st.title("NetDevOpsSupporter")
parser, regex, commander = st.tabs(["Parser", "Regex","Commander"])

with parser:
    st_parser(st)

with regex:
    st_regex(st)

with commander:
    st_commander(st)
