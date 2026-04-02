import streamlit as st
import pandas as pd
import os
import base64
import socket 
from datetime import datetime

# --- IMPORTACIÓN DE PÁGINAS ---
try:
    from Paginas.IMSSBI.Interfaz_IMSSBI import mostrar_interfaz_imssbi
    from Paginas.IMSSME.Interfaz_IMSSME import mostrar_interfaz_imssme
    from Paginas.NOMINA.Interfaz_Nomina_Azu import mostrar_interfaz_nomina_azu
except ImportError as e:
    st.error(f"Error al cargar los módulos de páginas: {e}")

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Admin TICS - Rancho Santa Rosa",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FUNCIONES DE APOYO ---
@st.cache_data
def get_base64_image(image_path):
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

# --- 3. ESTILOS CSS (TODO CENTRADO Y MEJORADO) ---
st.markdown("""
    <style>
    .stAppDeployButton {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main { background-color: #f8f9fa; }
    
    [data-testid="stSidebar"] { background-color: #0d1b2a; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    .centered-header { text-align: center; color: #1b263b; margin-bottom: 5px; }
    .centered-subtext { text-align: center; color: #6c757d; margin-bottom: 30px; }

    .metric-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 5px solid #1b263b;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .historial-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }
    .historial-card {
        background-color: white; padding: 15px; border-radius: 10px;
        border-left: 6px solid #1b263b; margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); width: 85%;
        text-align: center;
    }
    .version-container {
        text-align: center; color: #a3b18a; font-size: 0.8em;
        padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. BARRA LATERAL ---
with st.sidebar:
    logo_b64 = get_base64_image("Imagenes/SR.png")
    if logo_b64:
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_b64}" width="150"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Bienvenido</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a3b18a;'>Rancho Santa Rosa</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu = st.radio("Seleccione una sección:", 
                    ["📄 Información", "📕 IMSS Mensual", "📖 IMSS Bimestral", "🗓️ NÓMINA & SUA"],
                    key="menu_principal")
    
    st.markdown('<div class="version-container">Versión 1.1.5<br>TICS & Administración</div>', unsafe_allow_html=True)

# --- 5. INICIALIZAR SESSION STATE ---
if "historial_procesos" not in st.session_state:
    st.session_state["historial_procesos"] = []

# --- 6. NAVEGACIÓN ---
if menu == "📄 Información":
    _, col_centro, _ = st.columns([1, 2, 1])
    with col_centro:
        img_control_b64 = get_base64_image("Imagenes/control.png")
        if img_control_b64:
            st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_control_b64}" width="150"></div>', unsafe_allow_html=True)
        st.markdown("<h1 class='centered-header'>Gestión de Contador</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='centered-subtext'>Última actualización global: {leer_ultima_fecha()}</p>", unsafe_allow_html=True)

    st.divider()

    # MÉTRICAS
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="metric-card"><p style="color:gray;">ESTADO DEL SISTEMA</p><h2>Operativo ✅</h2></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(f'<div class="metric-card"><p style="color:gray;">SERVIDOR DE DATOS</p><h2>{verificar_conexion_internet()}</h2></div>', unsafe_allow_html=True)
    with col_c:
        # AQUÍ SE CALCULA EL NÚMERO DE PROCESOS REALES
        total_hoy = len(st.session_state["historial_procesos"])
        color_numero = "#2e7d32" if total_hoy > 0 else "#1b263b"
        st.markdown(f"""
            <div class="metric-card">
                <p style="color:gray;">PROCESOS HOY</p>
                <h2 style="color:{color_numero}; font-size: 48px;">{total_hoy}</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align: center;'>🕒 Actividad Reciente</h3>", unsafe_allow_html=True)
    
    st.markdown('<div class="historial-container">', unsafe_allow_html=True)
    if st.session_state["historial_procesos"]:
        for item in reversed(st.session_state["historial_procesos"]):
            st.markdown(f"""
            <div class="historial-card">
                <span style="color: #0d1b2a; font-weight: bold;">{item['tipo']}</span> | 
                <b>Archivo:</b> {item['archivo']} | 
                <span style="color: gray; font-size: 0.8em;">{item['hora']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        _, col_info, _ = st.columns([1, 2, 1])
        with col_info:
            st.info("No se han registrado movimientos en la sesión actual.")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📕 IMSS Mensual":
    mostrar_interfaz_imssme()
elif menu == "📖 IMSS Bimestral":
    mostrar_interfaz_imssbi()
elif menu == "🗓️ NÓMINA & SUA":
    mostrar_interfaz_nomina_azu()
