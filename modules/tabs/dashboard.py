import streamlit as st

def display():
    st.set_page_config(layout="wide", page_title="Dashboard", page_icon="📱")
    st.header("Dashboard Interactivo")
    looker = """
    <iframe style="width: 90vw; height: 80vh; background-color: lightblue;" src="https://lookerstudio.google.com/embed/reporting/233c975f-06ca-4a44-b630-61c0dbc06390/page/hcWRE"
     frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin 
     allow-popups allow-popups-to-escape-sandbox"></iframe>
    """
    st.markdown(looker, unsafe_allow_html=True)