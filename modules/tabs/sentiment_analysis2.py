import streamlit as st
import requests

def display():
    # Configurar el color de fondo de toda la aplicación
    st.markdown("""
        <style>
        .stApp {
            background-color: #F4F6FF;
            color:#387478;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Sentiment Analysis App")
    st.subheader("analisis de los sentimientos de los comentarios en ingles", divider="red")

    # Input para el comentario
    comentario = st.text_area("Ingrese su comentario:")

    # Botón para clasificar
    if st.button("Clasificar", type="primary"):
        # Enviar comentario a la API Flask
        response = requests.post('http://localhost:8080/api/classify', json={'comentario': comentario})

        if response.status_code == 200:
            # Obtener resultado de sentimiento
            resultado = response.json().get('resultado')
            if resultado == "Positivo":
                resultado += '😄'
            else:
                resultado += '😠'

            st.success(f"Resultado de la Clasificación: {resultado}")
        else:
            st.error("Error al clasificar el comentario.")