import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Dashboard IRD", layout="wide")


# --- Banner con Título a la izquierda y Logo a la derecha ---
col_logo, col_title = st.columns([8, 1])

with col_logo:
    st.markdown(
        """
        <div style='background-color:#003DA5; padding: 10px; border-radius: 5px;'>
            <h2 style='color:white; text-align:center;'>🌊 Dashboard Índice de Riesgo de Desastres (IRD) – Amenaza por Tsunami</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_title:
    st.image("images/logo.png", width=120)  # Ajusta el ancho si quieres que sea más grande o pequeño



# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
        .stApp {
            background-color: white;
        }
        h1, h2, h3, h4, p, li, label, .markdown-text-container {
            color: #0b1e34;  /* Azul oscuro */
            font-family: Calibri, sans-serif;
        }
        .stDownloadButton>button, .stButton>button {
            background-color: #1f6f8b;
            color: white;
            border-radius: 0.5rem;
            padding: 0.6rem 1rem;
            border: none;
        }
        .stDownloadButton>button:hover, .stButton>button:hover {
            background-color: #278ea5;
        }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
# --- PARÁMETROS DE ENTRADA ---
ird = st.slider("Selecciona el valor de IRD", 0, 100, 72)
amenaza = 85
vulnerabilidad = 65
resiliencia = 45

# --- GRÁFICO VELOCÍMETRO ---
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=ird,
    title={'text': "IRD Global (%)"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "black", 'thickness': 0.2},
        'steps': [
            {'range': [0, 40], 'color': "#d00000"},    # Rojo
            {'range': [40, 70], 'color': "#ffdd00"},   # Amarillo
            {'range': [70, 100], 'color': "#38b000"}   # Verde
        ]
    }
))
fig_gauge.update_layout(paper_bgcolor='white', font=dict(color="#0b1e34"))
st.plotly_chart(fig_gauge, use_container_width=True)

# --- GRÁFICO DE BARRAS ---
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(x=[amenaza], y=["Amenaza"], orientation='h', marker_color='#d00000'))
fig_bar.add_trace(go.Bar(x=[vulnerabilidad], y=["Vulnerabilidad"], orientation='h', marker_color='#ffdd00'))
fig_bar.add_trace(go.Bar(x=[resiliencia], y=["Resiliencia"], orientation='h', marker_color='#38b000'))
fig_bar.update_layout(
    title="Componentes del IRD (%)",
    xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
    barmode='stack',
    height=300,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#0b1e34")
)

# --- RADAR AMENAZA ---
radar_amenaza = [0.8, 0.6, 0.7, 0.9, 0.75]
labels_amenaza = ["Subfactor A1", "Subfactor A2", "Subfactor A3", "Subfactor A4", "Subfactor A5"]
fig_radar_1 = go.Figure()
fig_radar_1.add_trace(go.Scatterpolar(r=radar_amenaza, theta=labels_amenaza, fill='toself'))
fig_radar_1.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=False,
    title="Radar Amenaza",
    paper_bgcolor="white",
    font=dict(color="#0b1e34")
)

# --- RADAR RESILIENCIA ---
radar_resiliencia = [0.4, 0.5, 0.6, 0.3, 0.5]
labels_resiliencia = ["Subfactor R1", "Subfactor R2", "Subfactor R3", "Subfactor R4", "Subfactor R5"]
fig_radar_2 = go.Figure()
fig_radar_2.add_trace(go.Scatterpolar(r=radar_resiliencia, theta=labels_resiliencia, fill='toself'))
fig_radar_2.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=False,
    title="Radar Resiliencia",
    paper_bgcolor="white",
    font=dict(color="#0b1e34")
)

# --- DISTRIBUCIÓN DE GRÁFICOS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(fig_bar, use_container_width=True)
with col2:
    st.plotly_chart(fig_radar_1, use_container_width=True)
with col3:
    st.plotly_chart(fig_radar_2, use_container_width=True)

# --- INFORMACIÓN DEL PROYECTO ---
with st.expander("📍 Información del Proyecto"):
    st.markdown("""
    <ul>
        <li><strong>Nombre:</strong> CESFAM Costero</li>
        <li><strong>Región:</strong> Valparaíso</li>
        <li><strong>Comuna:</strong> El Quisco</li>
        <li><strong>Sector:</strong> Salud</li>
        <li><strong>Responsable:</strong> Seremi de Salud RM</li>
    </ul>
    """, unsafe_allow_html=True)

# --- RECOMENDACIONES AUTOMÁTICAS ---
st.markdown("### 📝 Recomendaciones Automáticas")
if ird > 60:
    st.error("RIESGO CRÍTICO: Reubicar el proyecto o incorporar obras de mitigación.")
elif ird > 30:
    st.warning("RIESGO MODERADO: Implementar medidas de reducción de vulnerabilidad y aumentar resiliencia.")
else:
    st.success("RIESGO ACEPTABLE: El proyecto puede avanzar con monitoreo.")

# --- EXPORTAR RESULTADOS ---
st.markdown("### 📁 Exportar Resultados")
col5, col6 = st.columns(2)
with col5:
    st.download_button("📄 Exportar PDF", "PDF generado...", file_name="IRD_resultado.pdf")
with col6:
    st.download_button("📊 Exportar Excel", "Excel generado...", file_name="IRD_resultado.xlsx")
