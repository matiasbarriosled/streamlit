import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.colors import sequential
from collections import Counter
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from gensim.parsing.preprocessing import STOPWORDS  # Stopwords de Gensim
from google.cloud import storage
from google.oauth2 import service_account
import os

# Configuración de PyTorch
os.environ['PYTORCH_JIT'] = '0'

# Cargar modelos de lenguaje
nlp = spacy.load("en_core_web_sm")
sia = SentimentIntensityAnalyzer()

# Credenciales de Google Cloud
credentials = service_account.Credentials.from_service_account_file(
    'env/utopian-honor-438417-u7-5b7f84fcfd25.json'
)
client = storage.Client(project='utopian-honor-438417-u7', credentials=credentials)

# Función para descargar archivo del bucket
def descargar_archivo(bucket_name, archivo_name):
    try:
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(archivo_name)
        archivo_local = f"./{archivo_name}"
        blob.download_to_filename(archivo_local)
        return archivo_local
    except Exception as e:
        st.error(f"Error al descargar el archivo {archivo_name}: {e}")
        raise

# Función para procesar reseñas y generar gráficos de pastel
def procesar_reseñas(reseñas, tipo):
    textos = reseñas['frase']
    complaints = {"Food": [], "Service": [], "Ambience": [], "Prices": [], "Organization": []}
    praise = {"Food": [], "Service": [], "Ambience": [], "Prices": []}
    
    for texto in textos.dropna():
        sentimiento = sia.polarity_scores(texto)
        doc = nlp(texto)
        for sent in doc.sents:
            if sentimiento["compound"] < 0:  # Reseñas negativas
                for token in sent:
                    if token.pos_ in ["NOUN", "ADJ"]:
                        if token.text.lower() in ["food", "meal", "dish", "cuisine"]:
                            complaints["Food"].append(token.text)
                        elif token.text.lower() in ["service", "staff", "waiter", "server"]:
                            complaints["Service"].append(token.text)
                        elif token.text.lower() in ["ambience", "atmosphere", "environment"]:
                            complaints["Ambience"].append(token.text)
                        elif token.text.lower() in ["price", "cost", "value"]:
                            complaints["Prices"].append(token.text)
                        elif token.text.lower() in ["organization", "management", "operation"]:
                            complaints["Organization"].append(token.text)
            elif sentimiento["compound"] > 0:  # Reseñas positivas
                for token in sent:
                    if token.pos_ in ["NOUN", "ADJ"]:
                        if token.text.lower() in ["ambience", "atmosphere", "environment"]:
                            praise["Ambience"].append(token.text)
                        elif token.text.lower() in ["food", "meal", "dish", "cuisine"]:
                            praise["Food"].append(token.text)
                        elif token.text.lower() in ["service", "staff", "waiter", "server"]:
                            praise["Service"].append(token.text)
                        elif token.text.lower() in ["price", "cost", "value"]:
                            praise["Prices"].append(token.text)

    if tipo == 'positivos':
        etiquetas = list(praise.keys())
        tamaños = [len(praise) for praise in praise.values()]
        colores = px.colors.sequential.Blues
    elif tipo == 'negativos':
        etiquetas = list(complaints.keys())
        tamaños = [len(complaints) for complaints in complaints.values()]
        colores = px.colors.sequential.Reds

    if sum(tamaños) == 0:
        st.warning(f"No hay datos suficientes para generar un gráfico de {tipo}.")
        return

    # Crear gráfico de pastel con Plotly
    fig = go.Figure(data=[go.Pie(
        labels=etiquetas,
        values=tamaños,
        hole=0.4,
        textinfo='label+percent',
        marker=dict(colors=px.colors.sequential.Blues if tipo == 'positivos' else px.colors.sequential.Reds)
       
    )])
    fig.update_layout(title=f"Frecuency of {'praise' if tipo == 'positivos' else 'complaints'}")

    st.plotly_chart(fig)

# Función para analizar y mostrar el resultado más importante gráficamente
def analizar_y_mostrar_principal(reseñas, tipo, top_n=5):
    textos = reseñas['frase']
    sustantivos_adjetivos = {}

    # Extraer sustantivos y adjetivos
    for texto in textos.dropna():
        doc = nlp(texto)
        for token in doc:
            if token.pos_ == "NOUN":  # Buscar sustantivos
                adjetivos = [child.text.lower() for child in token.children if child.pos_ == "ADJ"]
                if token.text.lower() not in sustantivos_adjetivos:
                    sustantivos_adjetivos[token.text.lower()] = adjetivos
                else:
                    sustantivos_adjetivos[token.text.lower()].extend(adjetivos)

    # Determinar el sustantivo más frecuente
    sustantivo_mas_relevante = max(sustantivos_adjetivos, key=lambda k: len(sustantivos_adjetivos[k]))
    adjetivos_asociados = sustantivos_adjetivos[sustantivo_mas_relevante]

    # Contar frecuencias de adjetivos
    adjetivos_frecuencias = Counter(adjetivos_asociados).most_common(5)  # Top 5 adjetivos más comunes
    adjetivos, frecuencias = zip(*adjetivos_frecuencias)  # Separar en listas

    total_adjetivos = sum(frecuencias)
    porcentajes = [freq / total_adjetivos * 100 for freq in frecuencias]

    # Crear gráfico de barras con Plotly
    fig = go.Figure(data=[go.Bar(
        x=adjetivos,
        y=frecuencias,
        text=[f"{p:.1f}%" for p in porcentajes],
        textposition='auto',
        marker_color='skyblue' if tipo == "praise" else 'salmon'
    )])
    fig.update_layout(
        title=f"{tipo.capitalize()} - of {sustantivo_mas_relevante}",
        xaxis_title="associated description",
        yaxis_title="Frecuency",
        xaxis=dict(tickangle=45)
    )
    
    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig)

    # Mostrar texto explicativo
    st.write(f"**{tipo.capitalize()}**: The most important noun is '{sustantivo_mas_relevante}', "
            f"frequently accompanied by description:")
    st.write(", ".join([f"{adj} ({porc:.1f}%)" for adj, porc in zip(adjetivos, porcentajes)]))

def generar_texto_final(reseñas_negativas):
    textos = reseñas_negativas['frase']
    sustantivos_adjetivos = {}

    # Extraer sustantivos y adjetivos de las reseñas negativas
    for texto in textos.dropna():
        doc = nlp(texto)
        for token in doc:
            if token.pos_ == "NOUN":  # Buscar sustantivos
                adjetivos = [child.text.lower() for child in token.children if child.pos_ == "ADJ"]
                if token.text.lower() not in sustantivos_adjetivos:
                    sustantivos_adjetivos[token.text.lower()] = adjetivos
                else:
                    sustantivos_adjetivos[token.text.lower()].extend(adjetivos)

    # Identificar el sustantivo más relevante y sus adjetivos asociados
    if not sustantivos_adjetivos:
        return "No se encontraron suficientes datos para generar un resumen de las quejas."

    sustantivo_mas_relevante = max(sustantivos_adjetivos, key=lambda k: len(sustantivos_adjetivos[k]))
    adjetivos_asociados = sustantivos_adjetivos[sustantivo_mas_relevante]

    # Determinar el adjetivo más frecuente
    if not adjetivos_asociados:
        adjetivo_mas_relevante = "no descriptions"
    else:
        adjetivo_mas_relevante = Counter(adjetivos_asociados).most_common(1)[0][0]

    # Crear el texto final
    texto_final = (
        f"Complaints are usually caused by {sustantivo_mas_relevante},"
        f" which is usually described as {adjetivo_mas_relevante}."
    )

    return texto_final

# Ejecución principal
try:
    st.write("Loading initial configuration...")
    bucket_name = 'review_main_cities'
    ciudades = ['Nueva York', 'California', 'Florida', 'Texas']
    archivo_dict = {
        'Nueva York': {'positivos': 'comentarios_positivos_NY.csv', 'negativos': 'comentarios_negativos_NY.csv'},
        'California': {'positivos': 'comentarios_positivos_CA.csv', 'negativos': 'comentarios_negativos_CA.csv'},
        'Florida': {'positivos': 'comentarios_positivos_FL.csv', 'negativos': 'comentarios_negativos_FL.csv'},
        'Texas': {'positivos': 'comentarios_positivos_TX.csv', 'negativos': 'comentarios_negativos_TX.csv'}
    }

    # Selección de ciudad
    ciudad_seleccionada = st.selectbox('Please select a city or state:', ciudades)
    st.write(f"You have selected: {ciudad_seleccionada}")

    # Botón para confirmar la selección
    if st.button("start analysis"):
        st.write("loading data...")
        archivo_bucket = archivo_dict[ciudad_seleccionada]

        archivo_positivos = descargar_archivo(bucket_name, archivo_bucket['positivos'])
        archivo_negativos = descargar_archivo(bucket_name, archivo_bucket['negativos'])
        st.success("Files uploaded successfully.")

        st.write("Processing uploaded data...")
        reseñas_positivas = pd.read_csv(archivo_positivos, on_bad_lines='warn')
        reseñas_negativas = pd.read_csv(archivo_negativos, on_bad_lines='warn')
        st.success("processed data.")

        st.write("Analyzing positive reviews...")
        procesar_reseñas(reseñas_positivas, 'positivos')
        st.success("Positive reviews analysis completed.")

        st.write("Analyzing negative reviews...")
        procesar_reseñas(reseñas_negativas, 'negativos')
        st.success("Negative reviews analysis completed.")

        st.write("Generating praise results...")
        analizar_y_mostrar_principal(reseñas_positivas, "alabanzas")
        st.success("Praise results generated.")

        st.write("Generating critique results...")
        analizar_y_mostrar_principal(reseñas_negativas, "críticas")
        st.success("Review results generated.")

        st.write("Generating final summary for complaints...")
        texto_final = generar_texto_final(reseñas_negativas)
        st.write(texto_final)

                # Resaltar el texto final
        st.markdown(
            f"""
            <div style="
                border: 2px solid #FF5733;
                padding: 20px;
                border-radius: 10px;
                background-color: #FFF3E6;
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


except Exception as e:
    st.error(f"Error: {e}")

