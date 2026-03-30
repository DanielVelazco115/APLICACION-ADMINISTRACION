import streamlit as st
import pandas as pd
import os
import base64
import socket 
from datetime import datetime
from Paginas.IMSSBI.Interfaz_IMSSBI import mostrar_interfaz_imssbi
from Paginas.IMSSME.Interfaz_IMSSME import mostrar_interfaz_imssme
from Paginas.NOMINA.Interfaz_Nomina_Azu import mostrar_interfaz_nomina_azu

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Admin TICS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FUNCIONES DE APOYO (OPTIMIZADAS) ---
@st.cache_data
def get_base64_image(image_path):
    """Carga y cachea imágenes para mejorar la velocidad."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def verificar_conexion_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return "Conectado 🌐"
    except OSError:
        return "Desconectado ❌"

FECHA_LOG = "fecha_modificacion.txt"
def leer_ultima_fecha():
    if os.path.exists(FECHA_LOG):
        with open(FECHA_LOG, "r") as f:
            return f.read()
    return "Sin registros previos"

# --- 3. ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Ocultar botones de Streamlit (Deploy y Menú) */
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilos de Contenedores */
    .main { background-color: #f5f7f9; }
    
    /* Centrado de Radio Buttons en Sidebar */
    div[data-testid="stRadio"] > label { 
        display: flex; justify-content: center; font-weight: bold; color: #004691; 
    }
    div[data-testid="stRadio"] div[role="radiogroup"] { 
        display: flex; flex-direction: column; align-items: center; 
    }

    /* Cards de Historial */
    .historial-card {
        background-color: white; padding: 12px 20px; border-radius: 10px;
        border-left: 6px solid #004691; margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Estilo para el Badge de Versión */
    .version-container {
        text-align: center; color: #6c757d; font-size: 0.9em;
        padding: 10px; border-top: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BARRA LATERAL ---
with st.sidebar:
    # Logo
    logo_b64 = get_base64_image("Imagenes/SR.png")
    if logo_b64:
        st.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{logo_b64}" width="120" style="margin-bottom: 10px;">
                <h2 style='margin-bottom: 0;'>Bienvenido</h2>
                <p style='margin-top: 0; color: #666;'>Rancho Santa Rosa</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    menu = st.radio(
        "¿Qué Sección Buscas?", 
        ["📄 Informacion", "📕 IMSS Mensual", "📖 IMSS Bimestral", "🗓️ NOMINA & SUA"],
        label_visibility="collapsed" # Ocultamos el label para usar el diseño central
    )
    
    st.divider()
    
    # Versión en el pie del sidebar
    st.markdown('<div class="version-container">Versión 1.1.5</div>', unsafe_allow_html=True)

# --- 5. LÓGICA DE NAVEGACIÓN ---

# Inicializar sesión
if "historial_procesos" not in st.session_state:
    st.session_state["historial_procesos"] = []

if menu == "📄 Informacion":
    # Header Principal
    img_control_b64 = get_base64_image("Imagenes/control.png")
    header_html = f"""
        <div style='display: flex; align-items: center; justify-content: center; gap: 25px; padding: 20px;'>
            {f'<img src="data:image/png;base64,{img_control_b64}" width="120">' if img_control_b64 else ""}
            <h1 style='margin: 0; color: #004691; font-family: sans-serif;'>Control Administrativo</h1>
        </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    st.divider()

    # Métricas
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        estado = "Operativo ✅" if mostrar_interfaz_imssme and mostrar_interfaz_imssbi else "Error ⚠️"
        st.metric("Estado del Sistema", estado)
    with col_b:
        st.metric("Servidor de Datos", verificar_conexion_internet())
    with col_c:
        total_hoy = len(st.session_state["historial_procesos"])
        st.metric("Procesos Hoy", total_hoy, delta=f"+{total_hoy}" if total_hoy > 0 else None)

    st.subheader("🕒 Actividad Reciente")
    
    if st.session_state["historial_procesos"]:
        for item in reversed(st.session_state["historial_procesos"]):
            st.markdown(f"""
            <div class="historial-card">
                <span style="color: #004691; font-weight: bold;">{item['tipo']}</span> | 
                <b>Archivo:</b> {item['archivo']} | 
                <span style="color: gray; font-size: 0.8em;">{item['hora']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No se han registrado procesos en esta sesión.")

    st.divider()
    st.caption(f"Última modificación global: {leer_ultima_fecha()}")

elif menu == "📕 IMSS Mensual":
    mostrar_interfaz_imssme()
elif menu == "📖 IMSS Bimestral":
    mostrar_interfaz_imssbi()
elif menu == "🗓️ NOMINA & SUA":
    mostrar_interfaz_nomina_azu()
