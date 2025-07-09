import streamlit as st
import geopandas as gpd
import zipfile
import os
import tempfile
import folium
from streamlit_folium import st_folium

col_1, col_2 = st.columns([8, 1])
with col_1:
    st.markdown(
        """
        <div style='background-color:#003DA5; padding: 10px; border-radius: 5px;'>
            <h2 style='color:white; text-align:center;'>🌊 Amenaza</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_2:
    st.image("images/logo.png", width=120)  # Ajusta el ancho si quieres que sea más grande o pequeño



st.write("Aquí se carga el archivo de curvas de tsunami y se calcula la amenaza.")

# --- Evitar ocultar texto
st.markdown("""
<style>
html, body, .stApp {
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# --- Archivos
uploaded_curves = st.file_uploader('Sube el archivo de curvas de altura de tsunami (KML/KMZ)', type=['kml', 'kmz'])
uploaded_project = st.file_uploader('Sube el polígono del proyecto (KML/KMZ)', type=['kml', 'kmz'])

def read_kml_or_kmz(uploaded_file):
    if uploaded_file.name.endswith('.kml'):
        return gpd.read_file(uploaded_file)
    elif uploaded_file.name.endswith('.kmz'):
        with tempfile.TemporaryDirectory() as tmpdirname:
            kmz_path = os.path.join(tmpdirname, 'temp.kmz')
            with open(kmz_path, 'wb') as f:
                f.write(uploaded_file.read())
            with zipfile.ZipFile(kmz_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdirname)
            for root, _, files in os.walk(tmpdirname):
                for name in files:
                    if name.endswith('.kml'):
                        return gpd.read_file(os.path.join(root, name))
    return None

amenaza_valores = {'Muy Alto': 1, 'Alto': 0.8426, 'Medio': 0.5579, 'Bajo': 0.101, 'Nulo': 0}
mapeo_categorias = {
    'Profundidad de la inundación: 6 y más': 'Muy Alto',
    'Profundidad de la inundación: 4 - 6': 'Muy Alto',
    'Profundidad de la inundación: 2 - 4': 'Alto',
    'Profundidad de la inundación: 1 - 2': 'Medio',
    'Profundidad de la inundación: 0.3 - 1': 'Bajo',
    'Sin inundación': 'Nulo'
}

categoria_amenaza = 'Nulo'
amenaza = 0
gdf_curves, gdf_project = None, None

if uploaded_curves:
    gdf_curves = read_kml_or_kmz(uploaded_curves)
    if gdf_curves is not None:
        gdf_curves = gdf_curves.to_crs(epsg=4326)

if uploaded_project:
    gdf_project = read_kml_or_kmz(uploaded_project)
    if gdf_project is not None:
        gdf_project = gdf_project.to_crs(epsg=4326)

        st.markdown("""<h5 style='text-align:center;'>Visualización del Proyecto</h5>""", unsafe_allow_html=True)
        m = folium.Map(location=[gdf_project.geometry.centroid.y.mean(), gdf_project.geometry.centroid.x.mean()], zoom_start=13)
        folium.GeoJson(gdf_project, style_function=lambda x: {'color': 'blue'}).add_to(m)
        if gdf_curves is not None:
            folium.GeoJson(gdf_curves, style_function=lambda x: {'color': 'red', 'weight': 1, 'fillOpacity': 0.1}).add_to(m)
        st_folium(m, width=600, height=400)

        # Cruce espacial
        
col11, col12= st.columns(2)
with col11:        
        if gdf_curves is not None:
            intersect = gdf_curves[gdf_curves.geometry.intersects(gdf_project.geometry.unary_union)]
            if not intersect.empty:
                categorias = intersect['Name'].unique().tolist()
                categorias_convertidas = [mapeo_categorias.get(c, 'Nulo') for c in categorias]
                categoria_amenaza = max(categorias_convertidas, key=lambda x: amenaza_valores.get(x, 0))
                amenaza = amenaza_valores[categoria_amenaza]
                st.success(f"Amenaza asignada: {categoria_amenaza} (valor: {amenaza})")
            else:
                st.warning("El polígono no intersecta ninguna zona de amenaza. Amenaza = Nulo.")

if gdf_curves is not None and gdf_project is not None:
    intersect = gdf_curves[gdf_curves.geometry.intersects(gdf_project.geometry.unary_union)]
    if not intersect.empty:
        folium.GeoJson(intersect, style_function=lambda x: {'color': 'green'}).add_to(m)

with col12:
# Enlace a CITSU
    st.markdown("""
<p style='font-size:12px;'>Puedes descargar las cartas <b>CITSU</b> en:<br>
<a href='https://www.shoa.cl/php/citsu.php' target='_blank'>https://www.shoa.cl/php/citsu.php</a></p>
""", unsafe_allow_html=True)

# Justificación
    Justificacion_amenaza = st.text_area("Justificación de la Amenaza (indicar fuente de información)", placeholder="Describe la justificación de la categoría de amenaza asignada...")
import uuid

if st.button("💾 Guardar Amenaza"):

    if 'usuario' not in st.session_state or not st.session_state.usuario:
        st.warning("⚠️ Debes iniciar sesión para guardar datos.")
        st.stop()

    if 'proyectos' not in st.session_state:
        st.session_state.proyectos = {}
    if st.session_state.usuario not in st.session_state.proyectos:
        st.session_state.proyectos[st.session_state.usuario] = []

    # Generar ID único para el proyecto
    nuevo_id = str(uuid.uuid4())[:8]

    # Tomar el valor correcto de amenaza (ya calculado)
    datos_amenaza = {
        'categoria_amenaza': categoria_amenaza,
        'valor_amenaza': amenaza,
        'justificacion_amenaza': Justificacion_amenaza
    }

    # Obtener nombre del proyecto si está definido en session_state
    nombre_proyecto = st.session_state.get('nombre_proyecto', f"Proyecto_{nuevo_id}")

    # Armar el proyecto (puede estar incompleto hasta que se agreguen vulnerabilidad y resiliencia)
    proyecto = {
        'ID': nuevo_id,
        'Nombre Proyecto': nombre_proyecto,
        'Amenaza': datos_amenaza
    }

    # Guardar el proyecto actual en sesión
    st.session_state.proyectos[st.session_state.usuario].append(proyecto)
    st.success(f"✅ Proyecto guardado con ID: {nuevo_id}")

import json
from utils.github_api import guardar_en_github

# Solo si ya existe proyecto_actual
if 'proyecto_actual' in st.session_state:
    proyecto_json = json.dumps(st.session_state.proyecto_actual, indent=2)
    nombre_archivo = f"{usuario}_proyecto_{st.session_state.proyecto_actual['ID']}.json"
    repo = "NOMBRE_DEL_REPO"
    usuario_github = "TU_USUARIO"
    token_github = st.secrets["github_token"]  # o directamente "ghp_xxx..." si no usas secrets

    exito = guardar_en_github(nombre_archivo, proyecto_json, repo, token_github, usuario_github)
    if exito:
        st.success("✅ Proyecto guardado también en GitHub")
    else:
        st.warning("⚠️ No se pudo guardar en GitHub")


