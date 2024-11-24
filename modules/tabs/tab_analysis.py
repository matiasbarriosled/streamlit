import streamlit as st
import pandas as pd
import os
from modules.functions.texto_final import generar_texto_final
from modules.functions.descargar_archivo import descargar_archivo
from modules.functions.procesar_resenias import procesar_resenias
from modules.functions.mostrar_principal import analizar_y_mostrar_principal
from streamlit_lottie import st_lottie
import requests

# Función para cargar el archivo Lottie
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

@st.dialog("Aguarde unos minutos mientras obtenemos la informacion")
def loading_wait():
    lottie_json = load_lottie_url(lottie_loading_url)
    st_lottie(lottie_json, speed=1, height=300)

def finalizado(placeholder):
    placeholder.empty()

# URL del archivo Lottie (puedes cambiar esta URL por la que prefieras)
lottie_loading_url = "https://lottie.host/ff4e35af-6352-4623-af91-f03c9fcc9b72/HpVz35CKey.json"
def display(ciudad_seleccionada):
    st.title(ciudad_seleccionada)
    try:
        bucket_name = 'review_main_cities'
        archivo_dict = {
            'New York': {'positivos': 'comentarios_positivos_NY.csv', 'negativos': 'comentarios_negativos_NY.csv'},
            'California': {'positivos': 'comentarios_positivos_CA.csv', 'negativos': 'comentarios_negativos_CA.csv'},
            'Florida': {'positivos': 'comentarios_positivos_FL.csv', 'negativos': 'comentarios_negativos_FL.csv'},
            'Texas': {'positivos': 'comentarios_positivos_TX.csv', 'negativos': 'comentarios_negativos_TX.csv'}
        }
        freq_praise, freq_compl, pos_words, neg_words, summary = st.tabs(["Frequency praise", "Frequency complaints", "Positive Words", "Negative Words", "Summary"])

        with freq_praise:
            placeholder = st.empty()
            with placeholder.container():
                loading_wait()
                st.write("loading data...")
                st.success("Files uploaded successfully.")
                archivo_bucket = archivo_dict[ciudad_seleccionada]
                archivo_positivos = descargar_archivo(bucket_name, archivo_bucket['positivos'])
                archivo_negativos = descargar_archivo(bucket_name, archivo_bucket['negativos'])
                st.write("Processing uploaded data...")
                reseñas_positivas = pd.read_csv(archivo_positivos, on_bad_lines='warn')
                reseñas_negativas = pd.read_csv(archivo_negativos, on_bad_lines='warn')
                st.success("Processed data.")
                st.write("Analyzing positive reviews...")
            procesar_resenias(reseñas_positivas, 'positivos')
            st.success("Positive reviews analysis completed.")
        with freq_compl:
            st.write("Analyzing negative reviews...")
            procesar_resenias(reseñas_negativas, 'negativos')
            st.success("Negative reviews analysis completed.")
        with pos_words:
            st.write("Generating praise results...")
            analizar_y_mostrar_principal(reseñas_positivas, "alabanzas")
            st.success("Praise results generated.")
        with neg_words:
            st.write("Generating critique results...")
            analizar_y_mostrar_principal(reseñas_negativas, "críticas")
            st.success("Review results generated.")
        with summary:
            st.write("Generating final summary for complaints...")
            st.image("source_media/sentiment-space.png")
            texto_final = generar_texto_final(reseñas_negativas)
            st.info(texto_final,icon="ℹ️")
            # Resaltar el texto final
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #FF7F3E;
                    padding: 40px;
                    border-radius: 10px;
                    background-color: #F6F7C4;
                    font-size: 1.2rem;
                    font-weight: bold;
                    color: #C70039;
                    text-align: center;
                ">
                    {texto_final}
                </div>
                """,
                unsafe_allow_html=True
            )
            finalizado(placeholder)

    except Exception as e:
        st.error(f"An error occurred: {e}")