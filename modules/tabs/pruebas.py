import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
def loading_wait():
    lottie_json = load_lottie_url(lottie_loading_url)
    st_lottie(lottie_json, speed=1, height=300)
# URL del archivo Lottie (puedes cambiar esta URL por la que prefieras)
lottie_loading_url = "https://lottie.host/ff4e35af-6352-4623-af91-f03c9fcc9b72/HpVz35CKey.json"


def finalizado(placeholder):
    time.sleep(4)
    placeholder.empty()

def display():
    # Placeholder para el mensaje
    placeholder = st.empty()
    with placeholder.container():
        loading_wait()
    
    finalizado(placeholder)
    