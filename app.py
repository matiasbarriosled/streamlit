import streamlit as st
from modules.tabs import tab_analysis
from modules.tabs import ingreso
from modules.tabs import dashboard
from modules.tabs import sentiment_analysis
from modules.tabs import select_city
from modules.tabs import pruebas

def get_value_city():
    return st.session_state.get('selected_city', None)  # aca esta el valor que cargamos en el script tab_analysis

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

def change_page(page_name):
    st.session_state.current_page = page_name

if st.session_state.current_page =="home":
        # Configuración de la página
    st.set_page_config(layout="wide", page_title="Sociuslab", page_icon="📱")
    
    # Barra lateral
    st.sidebar.title("Bienvenido GasCompany")
    #st.sidebar.image("source_media/sociuslab-icon-white.png", use_container_width=True)
    st.sidebar.write("Crecer sin límites")
    st.sidebar.write("Verifique el rubro acorde a su nivel de inversión.")
    if st.sidebar.button("Ingresar"):
        change_page("ingreso")
    elif st.sidebar.button("Dashboard Interactivo"):
        change_page("dashboard")
    elif st.sidebar.button("Analisis de comentarios"):
        change_page("sentiment_analysis")
    elif st.sidebar.button("Busqueda por ciudad"):
        change_page("select_city")
    #elif st.sidebar.button("prueba"):
    #    change_page("prueba")
    
    # Sección principal
    st.title("SOCIU​​SLAB")
    st.subheader("We help to create great business")

    # Layout de tres columnas
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.image("https://github.com/FJRB10/Final-Project-Henry-DSPT10/blob/main/app/source_media/detailed-main-page.png?raw=true",use_container_width=True)

    with col2:
        st.image("https://github.com/FJRB10/Final-Project-Henry-DSPT10/blob/main/app/source_media/sociuslab-icon-white-diff.png?raw=true",use_container_width=True)

    with col3:
        st.image("https://github.com/FJRB10/Final-Project-Henry-DSPT10/blob/main/app/source_media/review-main-page.png?raw=true", caption="Mockup del teléfono" ,use_container_width=True)


elif st.session_state.current_page == "ingreso":
    
    ingreso.display()

elif st.session_state.current_page =="dashboard":

    dashboard.display()

elif st.session_state.current_page == "sentiment_analysis":
    sentiment_analysis.display()

elif st.session_state.current_page == "select_city":
    select_city.display()

elif st.session_state.current_page == "analysis":
    tab_analysis.display(get_value_city())

#elif st.session_state.current_page == "prueba":
#    pruebas.display()