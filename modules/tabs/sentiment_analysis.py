import streamlit as st
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from keybert import KeyBERT
import pandas as pd

# Cargar el modelo BERT y tokenizer para clasificación de sentimientos
PATH = r"modelo_positivo_negativo.pth" # https://storage.googleapis.com/ml-bert-output/modelo_positivo_negativo.pth

class BERTSentimentClassifier(BertForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BERTSentimentClassifier.from_pretrained('bert-base-cased', num_labels=2)
model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')), strict=False)
model.eval()

# Cargar KeyBERT para la extracción de frases clave
kw_model = KeyBERT(model="distilbert-base-nli-mean-tokens")

# Función para clasificar un comentario como positivo o negativo
def clasificar_sentimiento(comentario):
    inputs = tokenizer(comentario, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    prediccion = torch.argmax(logits, dim=1).item()
    return "Positivo" if prediccion == 1 else "Negativo"

# Función para extraer palabras clave usando KeyBERT
def extraer_palabras_clave(comentarios, cantidad):
    texto_completo = ' '.join(comentarios)
    palabras = kw_model.extract_keywords(texto_completo, top_n=cantidad)
    return [palabra[0] for palabra in palabras]

def display():
    st.set_page_config(layout="wide", page_title="Clasificador", page_icon="📱")
    # Título de la aplicación
    st.title('Clasificador de Comentarios de Negocios')
    
    # Selección de ciudad
    ciudades = ['Houston', 'New York', 'Chicago', 'Los Angeles', 'Brooklyn', 
                'San Antonio', 'Dallas', 'Las Vegas', 'Miami', 'Philadelphia']
    ciudad_seleccionada = st.selectbox("Seleccione una ciudad", ciudades)
    
    # Ingresar el ID del establecimiento
    id_establecimiento = st.text_input("Ingrese el ID del negocio (business_id)")
    
    # Entrada para la cantidad de palabras clave
    cantidad_palabras = st.number_input("Ingrese la cantidad de palabras clave a extraer", min_value=1, value=5)
    
    # Botón para filtrar y procesar los comentarios
    if st.button("Procesar Comentarios"):
        if ciudad_seleccionada and id_establecimiento:
            # Cargar los DataFrames
            archivo_reviews = r"archivos/review_clean.json"  # https://storage.cloud.google.com/etl_prueba_4-11/data/data_city_filter/review_clean.json
            archivo_business = r"archivos/business_clean.json" # https://storage.cloud.google.com/consultabussines/business_clean.json
            
            df_reviews = pd.read_json(archivo_reviews, lines=True)
            df_business = pd.read_json(archivo_business, lines=True)
    
            # Buscar información del negocio en business_clean.json
            negocio = df_business[df_business['business_id'] == id_establecimiento]
            
            if not negocio.empty:
                # Extraer información del negocio
                nombre = negocio['name'].iloc[0]
                direccion = negocio['address'].iloc[0]
                ciudad = negocio['city'].iloc[0]
                estrellas = negocio['stars'].iloc[0]
                review_count = negocio['review_count'].iloc[0]
                atributos = negocio['attributes'].iloc[0]
                categorias = negocio['categories'].iloc[0]
                horarios = negocio['hours'].iloc[0]
    
                # Mostrar información del negocio
                st.subheader("Información del Negocio")
                st.write(f"**Nombre:** {nombre}")
                st.write(f"**Dirección:** {direccion}")
                st.write(f"**Ciudad:** {ciudad}")
                st.write(f"**Estrellas:** {estrellas}")
                st.write(f"**Cantidad de reseñas:** {review_count}")
                st.write(f"**Atributos:** {atributos}")
                st.write(f"**Categorías:** {categorias}")
                st.write(f"**Horarios:** {horarios}")
            else:
                st.warning("No se encontró información para el negocio con el ID proporcionado en business_clean.json.")
            
            # Filtrar los comentarios por el ID del negocio
            comentarios_negocio = df_reviews[df_reviews['business_id'] == id_establecimiento]
    
            if not comentarios_negocio.empty:
                # Calcular fechas más antigua y reciente
                fecha_mas_antigua = comentarios_negocio['date'].min()
                fecha_mas_reciente = comentarios_negocio['date'].max()
    
                # Filtrar comentarios con 4 o 5 estrellas
                comentarios_altas_estrellas = comentarios_negocio[comentarios_negocio['stars'] >= 4]
                cantidad_altas_estrellas = len(comentarios_altas_estrellas)
    
                # Mostrar estadísticas iniciales
                st.subheader("Estadísticas de los Comentarios")
                st.write(f"**Fecha más antigua del comentario:** {fecha_mas_antigua}")
                st.write(f"**Fecha más reciente del comentario:** {fecha_mas_reciente}")
                st.write(f"**Cantidad de comentarios con 4 o 5 estrellas:** {cantidad_altas_estrellas}")
    
                # Obtener lista de comentarios
                comentarios_filtrados = comentarios_negocio['text'].dropna().tolist()
    
                # Clasificar comentarios como positivos o negativos
                positivos = []
                negativos = []
                for comentario in comentarios_filtrados:
                    clasificacion = clasificar_sentimiento(comentario)
                    if clasificacion == "Positivo":
                        positivos.append(comentario)
                    else:
                        negativos.append(comentario)
    
                # Extraer palabras clave
                palabras_clave_positivos = extraer_palabras_clave(positivos, cantidad_palabras)
                palabras_clave_negativos = extraer_palabras_clave(negativos, cantidad_palabras)
    
                # Mostrar los primeros 5 comentarios positivos
                st.subheader("Comentarios Positivos (primeros 5)")
                for idx, comentario in enumerate(positivos[:5]):  # Limitar a 5 comentarios
                    st.write(f"Comentario {idx+1}: {comentario}")
    
                st.subheader(f"Palabras Clave en Comentarios Positivos (Top {cantidad_palabras})")
                st.write(', '.join(palabras_clave_positivos))
    
                # Mostrar los primeros 5 comentarios negativos
                st.subheader("Comentarios Negativos (primeros 5)")
                for idx, comentario in enumerate(negativos[:5]):  # Limitar a 5 comentarios
                    st.write(f"Comentario {idx+1}: {comentario}")
    
                st.subheader(f"Palabras Clave en Comentarios Negativos (Top {cantidad_palabras})")
                st.write(', '.join(palabras_clave_negativos))
            else:
                st.warning("No se encontraron comentarios para el ID del negocio proporcionado en reviews_clean.json.")
        else:
            st.warning("Por favor seleccione una ciudad e ingrese un ID de negocio.")
    