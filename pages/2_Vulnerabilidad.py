# Página: Vulnerabilidad
import streamlit as st



col_1, col_2 = st.columns([8, 1])
with col_1:
    st.markdown(
        """
        <div style='background-color:#003DA5; padding: 10px; border-radius: 5px;'>
            <h2 style='color:white; text-align:center;'>⚠️ Vulnerabilidad</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_2:
    st.image("images/logo.png", width=120)  # Ajusta el ancho si quieres que sea más grande o pequeño



st.write("Formulario para evaluar vulnerabilidad física, funcional y social.")

# Encabezado
st.markdown("""
<p style='font-size:20px; font-weight:bold; text-align:left;'>2.2 VULNERABILIDAD</p>
<p style='font-size:14px; text-align:justify;'>Selecciona la escala que corresponde para cada subfactor de Vulnerabilidad Física, Funcional y Social.</p>
""", unsafe_allow_html=True)

st.markdown("""
<p style='font-size:12px; text-align:justify;'>Puedes descargar el 
<a href='https://sni.gob.cl/storage/docs/Manual_de_escalas_IRD_amenaza_por_Tsunami_-sep2022.pdf' target='_blank'>
Manual de Escalas IRD - Tsunami</a></p>
""", unsafe_allow_html=True)

vulnerabilidad_pesos = []
vulnerabilidad_valores = []
criticidad = 'Alto'

col1, col2, col3 = st.columns(3)

# --- Columna 1: Vulnerabilidad Física ---
with col1:
    st.markdown("""<p style='font-size:14px; font-weight:bold; color:#004080;'>a) VULNERABILIDAD FÍSICA</p>""", unsafe_allow_html=True)
    subfactores_fisica = [
        ('Material estructura principal', 0.174534907, {'Seleccionar escala': 0, 'Alto': 1, 'Moderado': 0.53, 'Bajo': 0.22, 'Sin Información': 1}),
        ('Estado actual', 0.104720944, {'Seleccionar escala': 0, 'Malo': 1, 'Bueno': 0, 'Obra Nueva': 0, 'Sin Información': 1}),
        ('Plan de mantenimiento', 0.032206441, {'Seleccionar escala': 0, 'No': 1, 'Si': 0, 'Sin Información': 1})
    ]
    for nombre, peso, opciones in subfactores_fisica:
        st.markdown(f"<p style='font-size:14px;text-align:left;'>{nombre}</p>", unsafe_allow_html=True)
        seleccion = st.selectbox("", list(opciones.keys()), key=f'fis_{nombre}')
        vulnerabilidad_pesos.append(peso)
        vulnerabilidad_valores.append(opciones[seleccion])

# --- Columna 2: Vulnerabilidad Funcional ---
with col2:
    st.markdown("""<p style='font-size:14px; font-weight:bold; color:#004080;'>b) VULNERABILIDAD FUNCIONAL</p>""", unsafe_allow_html=True)
    subfactores_funcional = [
        ('Criticidad del servicio', 0.24964993, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.7157, 'Bajo': 0.3461, 'No crítico': 0.1344}),
        ('Incidencia del servicio en la economía local', 0.083216643, {'Seleccionar escala': 0, 'Alto': 1, 'Medio': 0.2154, 'Baja': 0.116, 'Sin Incidencia': 0, 'Sin Información': 1})
    ]
    for nombre, peso, opciones in subfactores_funcional:
        st.markdown(f"<p style='font-size:14px;text-align:left;'>{nombre}</p>", unsafe_allow_html=True)
        seleccion = st.selectbox("", list(opciones.keys()), key=f'fun_{nombre}')
        vulnerabilidad_pesos.append(peso)
        vulnerabilidad_valores.append(opciones[seleccion])

# --- Columna 3: Vulnerabilidad Social ---
with col3:
    st.markdown("""<p style='font-size:14px; font-weight:bold; color:#004080;'>c) VULNERABILIDAD SOCIAL</p>""", unsafe_allow_html=True)
    subfactores_social = [
        ('Grupos etarios vulnerables', 0.052710542, {'Seleccionar escala': 0, 'Personas dependientes': 1, 'Niño o adolescentes': 0.6711, 'Adultos': 0, 'Sin Información': 1}),
        ('Dependencia física población', 0.037507502, {'Seleccionar escala': 0, 'Atiende': 1, 'No atiende': 0, 'Sin Información': 1}),
        ('Población afectada', 0.133626725, {'Seleccionar escala': 0, 'Muy alto': 1, 'Alto': 0.6968, 'Medio': 0.3742, 'Bajo': 0.1987, 'Muy bajo': 0.0869, 'Sin Información': 1}),
        ('Pobreza por ingresos', 0.065913183, {'Seleccionar escala': 0, 'Alto': 1, 'Moderado': 0.6357, 'Bajo': 0.1005, 'Nulo': 0, 'Sin Información': 1}),
        ('Pobreza multidimensional', 0.065913183, {'Seleccionar escala': 0, 'Alto': 1, 'Moderado': 0.6357, 'Bajo': 0.1005, 'Nulo': 0, 'Sin Información': 1})
    ]
    for nombre, peso, opciones in subfactores_social:
        st.markdown(f"<p style='font-size:14px;text-align:left;'>{nombre}</p>", unsafe_allow_html=True)
        seleccion = st.selectbox("", list(opciones.keys()), key=f'soc_{nombre}')
        vulnerabilidad_pesos.append(peso)
        vulnerabilidad_valores.append(opciones[seleccion])

# --- Cálculo total de vulnerabilidad ---
vulnerabilidad = sum([p * v for p, v in zip(vulnerabilidad_pesos, vulnerabilidad_valores)])

# --- Enlace adicional ---
st.markdown("""
<p style='font-size:12px; text-align:justify;'>Puedes descargar la 
<a href='https://observatorio.ministeriodesarrollosocial.gob.cl/pobreza-comunal-2022' target='_blank'>
Estimación de Pobreza Comunal 2022</a></p>
""", unsafe_allow_html=True)

# --- Justificación final ---
Justificacion_vul = st.text_area("Justificación Vulnerabilidad")

if st.button("💾 Guardar Vulnerabilidad"):
    st.session_state['vulnerabilidad_data'] = {
        'vulnerabilidad': valor_total_vul,
        'vuln_df': df_vulnerabilidad,
        'justificacion_vul': justificacion_vul
    }
    st.success("✅ Vulnerabilidad guardada correctamente")

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
