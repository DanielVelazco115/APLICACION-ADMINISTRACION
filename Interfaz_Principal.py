import streamlit as st
import pandas as pd
import os
import base64
import socket 
from datetime import datetime
from Paginas.IMSSBI.Interfaz_IMSSBI import mostrar_interfaz_imssbi
from Paginas.IMSSME.Interfaz_IMSSME import mostrar_interfaz_imssme
from Paginas.NOMINA.Interfaz_Nomina_Azu import mostrar_interfaz_nomina_azu

# 1. Configuración de la página
st.set_page_config(
    page_title="Admin TICS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FUNCIONES DE APOYO REALES ---
FECHA_LOG = "fecha_modificacion.txt"

def verificar_conexion_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return "Conectado 🌐"
    except OSError:
        return "Desconectado ❌"

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

def leer_ultima_fecha():
    if os.path.exists(FECHA_LOG):
        with open(FECHA_LOG, "r") as f:
            return f.read()
    return "Sin registros previos"

# --- INICIALIZAR MEMORIA DE SESIÓN ---
if "historial_procesos" not in st.session_state:
    st.session_state["historial_procesos"] = []

# CSS mejorado para centrado total
st.markdown("""
    <style>
    /* Centrar navegación y radio buttons */
    [data-testid="stSidebarNav"] { text-align: center; }
    div[data-testid="stRadio"] > label { display: flex; justify-content: center; font-weight: bold; }
    div[data-testid="stRadio"] div[role="radiogroup"] { display: flex; flex-direction: column; align-items: center; }
    
    /* Estilos generales */
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .historial-card {
        background-color: white; padding: 10px 20px; border-radius: 8px;
        border-left: 5px solid #004691; margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Barra Lateral CENTRADA
with st.sidebar:
    # Imagen centrada
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("Imagenes/SR.png", use_container_width=True)
    
    # Títulos centrados con HTML
    st.markdown("""
        <div style='text-align: center;'>
            <h2 style='margin-bottom: 0;'>Bienvenido</h2>
            <h4 style='margin-top: 0; font-weight: normal;'>Rancho Santa Rosa</h4>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.sidebar.radio(
        "¿Qué Sección Buscas?", 
        ["📄 Informacion", "📕 IMSS Mensual", "📖 IMSS Bimestral", "🗓️ NOMINA & SUA"]
    )
    
    st.markdown("---")
    
    # Versión centrada
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.info("Versión 1.1.5")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. Cuerpo Principal ---
if menu == "📄 Informacion":
    img_control_b64 = get_base64_image("Imagenes/control.png")
    
    if img_control_b64:
        st.markdown(
            f"""
            <div style='text-align: center; display: flex; align-items: center; justify-content: center; gap: 20px;'>
                <img src='data:image/png;base64,{img_control_b64}' width='150'>
                <h1 style='margin: 0; color: #004691;'>Control Administrativo - Rancho Santa Rosa</h1>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        estado_sistema = "Operativo ✅" if mostrar_interfaz_imssme and mostrar_interfaz_imssbi else "Error Módulos ⚠️"
        st.metric("Estado del Sistema", estado_sistema)
    with col_b:
        status_red = verificar_conexion_internet()
        st.metric("Servidor de Datos", status_red)
    with col_c:
        total_hoy = len(st.session_state["historial_procesos"])
        st.metric("Procesos en esta sesión", total_hoy, delta=f"+{total_hoy}" if total_hoy > 0 else None)

    st.markdown("---")
    st.subheader("🕒 Actividad Reciente de la Sesión")
    
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
        st.info("No se han realizado procesos en esta sesión todavía.")

    st.markdown("---")
    fecha_mostrar = leer_ultima_fecha()
    st.info(f"Última modificación global detectada: {fecha_mostrar}")

elif menu == "📕 IMSS Mensual":
    mostrar_interfaz_imssme()
elif menu == "📖 IMSS Bimestral":
    mostrar_interfaz_imssbi()
elif menu == "🗓️ NOMINA & SUA":
    mostrar_interfaz_nomina_azu()
