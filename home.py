import streamlit as st

st.title("NetDevOpsSupporter")
if st.button("Parser"):
    st.switch_page("pages/parse.py")
if st.button("Regex"):
    st.switch_page("pages/regex.py")
