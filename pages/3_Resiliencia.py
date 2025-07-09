# Página: Resiliencia
import streamlit as st





col_1, col_2 = st.columns([8, 1])
with col_1:
    st.markdown(
        """
        <div style='background-color:#003DA5; padding: 10px; border-radius: 5px;'>
            <h2 style='color:white; text-align:center;'>🛠️ Resiliencia</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_2:
    st.image("images/logo.png", width=120)  # Ajusta el ancho si quieres que sea más grande o pequeño


st.write("Formulario para evaluar resiliencia física, funcional y local.")

# Encabezado
st.markdown("""
<p style='font-size:20px; font-weight:bold; text-align:left;'>2.3 RESILIENCIA</p>
<p style='font-size:14px; text-align:justify;'>Selecciona la escala correspondiente para cada subfactor de Resiliencia física, funcional y local.</p>
""", unsafe_allow_html=True)

resiliencia_fisica_pesos = []
resiliencia_fisica_valores = []
resiliencia_funcional_pesos = []
resiliencia_funcional_valores = []
resiliencia_local_pesos = []
resiliencia_local_valores = []

col1, col2, col3 = st.columns(3)

# --- Columna 1: Resiliencia Física ---
with col1:
    st.markdown("""<p style='font-size:14px; font-weight:bold; color:#004080;'>a) CAPACIDAD FÍSICA</p>""", unsafe_allow_html=True)
    subfactores_fisica_res = [
        ('Infraestructura protección proyecto', 0.100698603, {
            'Seleccionar escala': 0,
            'Tiene': 1,
            'No tiene': 0,
            'Sin Información': 0
        }),
        ('Obras protección externas', 0.157085828, {
            'Seleccionar escala': 0,
            'Tiene': 1,
            'No tiene': 0,
            'Sin Información': 0
        })
    ]
    for nombre, peso, opciones in subfactores_fisica_res:
        st.markdown(f"<p style='font-size:14px;text-align:left;'>{nombre}</p>", unsafe_allow_html=True)
        seleccion = st.selectbox("", list(opciones.keys()), key=f'res_fis_{nombre}')
        resiliencia_fisica_pesos.append(peso)
        resiliencia_fisica_valores.append(opciones[seleccion])

# --- Columna 2: Resiliencia Funcional ---
with col2:
    st.markdown("""<p style='font-size:14px; font-weight:bold; color:#004080;'>b) RESILIENCIA FUNCIONAL</p>""", unsafe_allow_html=True)
    subfactores_funcional_res = [
        ('Plan de continuidad operacional', 0.043812375, {
            'Seleccionar escala': 0,
            'Tiene': 1,
            'No tiene': 0,
            'Sin Información': 0
        }),
        ('Autonomía servicios básicos', 0.228043912, {
            'Seleccionar escala': 0,
            'Alta': 1,
            'Moderada': 0.7223,
            'Baja': 0.347,
            'Nulo': 0,
            'Sin Información': 0
        }),
        ('Conectividad servicio', 0.108882236, {
            'Seleccionar escala': 0,
            'Alto': 1,
            'Medio': 0.333,
            'Bajo': 0,
            'Sin Información': 0
        }),
        ('Redundancia sistema', 0.256986028, {
            'Seleccionar escala': 0,
            'Alto': 1,
            'Medio': 0.6705,
            'Bajo': 0.3199,
            'Nulo': 0,
            'Sin Información': 0
        })
    ]
    for nombre, peso, opciones in subfactores_funcional_res:
        st.markdown(f"<p style='font-size:14px;text-align:left;'>{nombre}</p>", unsafe_allow_html=True)
        seleccion = st.selectbox("", list(opciones.keys()), key=f'res_fun_{nombre}')
        resiliencia_funcional_pesos.append(peso)
        resiliencia_funcional_valores.append(opciones[seleccion])

# --- Columna 3: Resiliencia Local ---
with col3:
    st.markdown("""<p style='font-size:14px; font-weight:bold; color:#004080;'>c) RESILIENCIA LOCAL</p>""", unsafe_allow_html=True)
    subfactores_local_res = [
        ('Plan de gestión riesgo local', 0.104491018, {
            'Seleccionar escala': 0,
            'Alto': 1,
            'Medio': 0.1319,
            'Bajo': 0,
            'Sin Información': 0
        })
    ]
    for nombre, peso, opciones in subfactores_local_res:
        st.markdown(f"<p style='font-size:14px;text-align:left;'>{nombre}</p>", unsafe_allow_html=True)
        seleccion = st.selectbox("", list(opciones.keys()), key=f'res_loc_{nombre}')
        resiliencia_local_pesos.append(peso)
        resiliencia_local_valores.append(opciones[seleccion])

# --- Cálculo total de resiliencia ---
resiliencia_fisica = sum([p * v for p, v in zip(resiliencia_fisica_pesos, resiliencia_fisica_valores)])
resiliencia_funcional = sum([p * v for p, v in zip(resiliencia_funcional_pesos, resiliencia_funcional_valores)])
resiliencia_local = sum([p * v for p, v in zip(resiliencia_local_pesos, resiliencia_local_valores)])
resiliencia = resiliencia_fisica + resiliencia_funcional + resiliencia_local

# --- Justificación final ---
Justificacion_res = st.text_area("Justificación Resiliencia")


if st.button("💾 Guardar Resiliencia"):
    st.session_state['resiliencia_data'] = {
        'resiliencia': valor_total_res,
        'res_df': df_resiliencia,
        'justificacion_res': justificacion_res
    }
    st.success("✅ Resiliencia guardada correctamente")

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
