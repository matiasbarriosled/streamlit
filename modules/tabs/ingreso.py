import streamlit as st

def display():
    st.subheader("Seleccione el Rubro")
    rubros = ["Gastronomia", "Rubro 2"]
    selected_rubro = st.selectbox("Rubros disponibles:", rubros)

    st.subheader("Ciudades Cubiertas")
    NYcity="source_media/ciudades/New York.png"
    CHcity="source_media/ciudades/Illinois.png"
    MIcity="source_media/ciudades/Florida.png"
    LAcity="source_media/ciudades/California.png"
    LVcity="source_media/ciudades/Nevada.png"
    HOcity="source_media/ciudades/Houston.png"
    BRcity="source_media/ciudades/Brooklyn.png"
    SAcity="source_media/ciudades/San Antonio.png"
    DAcity="source_media/ciudades/Texas.png"
    PHcity="source_media/ciudades/Pensilvania.png"



    city = ['New York','Chicago','Miami','Los Angeles','Las Vegas','Houston','Brooklyn','San Antonio','Dallas','Philadelphia']
    pictures = [NYcity,CHcity,MIcity,LAcity,LVcity,
                HOcity,BRcity,SAcity,DAcity,PHcity,]
    
    selected_buttons, cities = st.columns([1,3]) 

    # Estilo personalizado para la tarjeta seleccionada
    selected_style = """
        <div style="
            border: 3px solid #740938;
            border-radius: 10px;
            background: linear-gradient(45deg, #FF9C73, #FF4545);
            padding: 10px;
            text-align: center;
            color: black">
        """
    default_style = """
        <div style="
            border: 1px solid #001;
            border-radius: 20px;
            padding: 20px;
            text-align: center;">
        """
    with selected_buttons:
        selected_city = st.radio("Selecciona una ciudad:", city, index=0)
    with cities:    
        for i in range(0, len(city), 5):
            cols = st.columns(5)
            for col, ciudad, picture in zip(cols, city[i:i + 5], pictures[i:i + 5]):
                with col:
                    style = selected_style if ciudad == selected_city else default_style
            
                    st.markdown(f"{style}<br><strong>{ciudad}</strong>", unsafe_allow_html=True)
                    st.image(picture, use_container_width=True, channels="BGR")
                    if ciudad == selected_city:
                        st.markdown("- SELECTED CITY ✅")

    if st.button("Busqueda"):
        change_page("busqueda")

    camara = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjpgaacwoWzBX_6Gvn_EEITr2Iz5srXYE34Q&s"
    cerebro = "data:image/jpeg;base64,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"

    @st.dialog("Elige una imagen")
    def imagen(img):
        st.image(img)
        if st.button("Activar"):
            pass
            
    if "imagen" not in st.session_state:
        st.write("elige una imagen")
        if st.button("camara"):
            imagen(camara)
        if st.button("cerebro"):
            imagen(cerebro)

