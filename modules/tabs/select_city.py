import streamlit as st
import os

def load_css(css_file):
    with open(os.path.join(os.path.dirname(__file__), css_file), 'r') as f:
        css = f.read()
    return css

def display():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "select_city"

    if "selected_city" not in st.session_state:
        st.session_state.selected_city = None
    def set_value(value):
        st.session_state.selected_city = value  # importante! esto va a almacenar en la sesion el valor seleccionado

    def change_page(page_name):
        st.session_state.current_page = page_name
        
    if st.session_state.current_page =="select_city":
        st.set_page_config(layout="wide")
        css = load_css("estilos/analysis.css")

        st.markdown(f"""
            <style>
                {css}
            </style>
        """, unsafe_allow_html=True)

        categorias = ["Gastronomia", "categoria2", "categoria3"]
        categoria_seleccionada = st.selectbox("", categorias)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            if st.button("New York", key="btn_ny", use_container_width=True):
                set_value("New York")
                change_page("analysis")
            st.image("source_media/ciudades/New York.png", caption="New York", use_container_width=True)

        with col2:
            if st.button("California", key="btn_cl", use_container_width=True):
                set_value("California")
                change_page("analysis")
            st.image("source_media/ciudades/California.png", caption="California", use_container_width=True)

        with col3:
            if st.button("Florida", key="btn_fl", use_container_width=True):
                set_value("Florida")
                change_page("analysis")
            st.image("source_media/ciudades/Florida.png", caption="Florida", use_container_width=True)

        with col4:
            if st.button("Texas", key="btn_tx", use_container_width=True):
                set_value("Texas")
                change_page("analysis")
            st.image("source_media/ciudades/Texas.png", caption="Texas", use_container_width=True)

        with col5:
            if st.button("Brooklyn", disabled=True, key="btn_bk", use_container_width=True):
                pass
            st.image("source_media/ciudades/Brooklyn.png", caption="Brooklyn", use_container_width=True)

        col6, col7, col8, col9, col10 = st.columns(5)

        with col6:
            if st.button("Houston", disabled=True, key="btn_hs", use_container_width=True):
                pass
            st.image("source_media/ciudades/Houston.png", caption="Houston", use_container_width=True)

        with col7:
            if st.button("Illinois", disabled=True, key="btn_il", use_container_width=True):
                pass
            st.image("source_media/ciudades/Illinois.png", caption="Illinois", use_container_width=True)

        with col8:
            if st.button("Nevada", disabled=True, key="btn_nv", use_container_width=True):
                pass
            st.image("source_media/ciudades/Nevada.png", caption="Nevada", use_container_width=True)

        with col9:
            if st.button("Pensilvania", disabled=True, key="btn_pn", use_container_width=True):
                pass
            st.image("source_media/ciudades/Pensilvania.png", caption="Pensilvania", use_container_width=True)

        with col10:
            if st.button("San Antonio", disabled=True, key="btn_sa", use_container_width=True):
                pass
            st.image("source_media/ciudades/San Antonio.png", caption="San Antonio", use_container_width=True)


#'categoria1': ['New York', 'California', 'Texas', 'Florida', 'Pensilvania', 'Nevada', 'Broklyn', 'Houston', 'San Antonio', 'Illinois'],