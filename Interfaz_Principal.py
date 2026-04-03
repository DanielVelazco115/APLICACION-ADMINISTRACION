import streamlit as st
import pandas as pd
import os
import base64
import socket 
import platform
import psutil
import pytz 
from datetime import datetime

# --- IMPORTACIÓN DE PÁGINAS ---
try:
    from Paginas.IMSSBI.Interfaz_IMSSBI import mostrar_interfaz_imssbi
    from Paginas.IMSSME.Interfaz_IMSSME import mostrar_interfaz_imssme
    from Paginas.NOMINA.Interfaz_Nomina_Azu import mostrar_interfaz_nomina_azu
    from Paginas.USUARIOSRE.Interfaz_Registro import mostrar_interfaz_registro 
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

def obtener_hora_mexico():
    tz = pytz.timezone('America/Mexico_City')
    return datetime.now(tz)

def obtener_clima_ficticio():
    return "☀️ 28°C - Rancho Santa Rosa, MX"

def guardar_usuario_permanente(nombre):
    """Guarda el nombre en el archivo log físico"""
    ahora = obtener_hora_mexico().strftime("%d/%m/%Y %H:%M:%S")
    with open("registro_usuarios.txt", "a", encoding="utf-8") as f:
        f.write(f"{ahora} | {nombre}\n")

@st.cache_data
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def obtener_pdf_base64(pdf_path):
    """Convierte el PDF a Base64 para el menú flotante"""
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')
    return None

def verificar_conexion_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return "Conectado 🌐"
    except OSError:
        return "Desconectado ❌"

def obtener_info_sistema():
    so = platform.system()
    nombre_pc = platform.node()
    
    if so == "Linux":
        so_display = "SERVIDOR CLOUD"
        icono = "☁️"
        id_display = "Streamlit Node"
    else:
        so_display = so
        icono = "🪟" if so == "Windows" else "🍎" if so == "Darwin" else "🐧"
        id_display = nombre_pc
    
    if so == "Darwin": so_display = "macOS"
    return f"{icono} {so_display}", id_display, "N/A"

FECHA_LOG = "fecha_modificacion.txt"
def leer_ultima_fecha():
    if os.path.exists(FECHA_LOG):
        with open(FECHA_LOG, "r") as f:
            return f.read()
    return "Sin registros previos"

# --- 3. LÓGICA DE RECURSOS (PDF Y FONDO) ---
# Cambia esta ruta si el nombre de tu manual es diferente
nombre_archivo_pdf = "Documentos/OL3000RTXL2U.pdf"
pdf_b64 = obtener_pdf_base64(nombre_archivo_pdf) 
link_pdf = f'data:application/pdf;base64,{pdf_b64}' if pdf_b64 else "#"

fondo_base64 = get_base64_image("Imagenes/Log2.jpg") 

# --- 4. ESTILOS CSS - TU DISEÑO ORIGINAL + MENÚ FLOTANTE ---
if fondo_base64:
    st.markdown(f"""
        <style>
        /* TUS ESTILOS ORIGINALES DE FONDO */
        [data-testid="stAppViewContainer"] {{
            background-color: #f8f9fa !important;
            background-image: linear-gradient(rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0.4)), 
                              url("data:image/jpg;base64,{fondo_base64}") !important;
            background-position: 130% center !important; 
            background-repeat: no-repeat !important;
            background-size: 1910px auto !important;
            background-attachment: fixed !important;
        }}

        [data-testid="stMainViewContainer"], .main, .block-container {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        [data-testid="stHeader"] {{ background: transparent !important; }}
        .stAppDeployButton {{display: none !important;}}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        [data-testid="stSidebar"] {{ background-color: #0d1b2a; }}
        [data-testid="stSidebar"] input {{ color: #0d1b2a !important; caret-color: #0d1b2a !important; }}
        [data-testid="stSidebar"] label p, [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] h3 {{ color: white !important; }}
        .version-container {{ text-align: center; color: #a3b18a !important; font-size: 0.8em; padding: 20px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 30px; }}
        .metric-card {{ background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; border-bottom: 5px solid #1b263b; min-height: 150px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .stButton>button {{ width: 100%; border-radius: 8px; background-color: #c1121f; color: white; border: none; transition: 0.3s; display: block; margin: 0 auto; }}
        .stButton>button:hover {{ background-color: #780001; color: white; }}

        /* NUEVO: ESTILOS DEL MENÚ FLOTANTE (AISLADOS) */
        .floating-container-rsr {{
            position: fixed; right: -160px; top: 25%; transition: 0.3s ease-in-out;
            padding: 15px; width: 200px; background-color: #1b263b;
            color: white !important; border-radius: 10px 0 0 10px; z-index: 999999;
            box-shadow: -2px 2px 10px rgba(0,0,0,0.3); font-family: sans-serif;
        }}
        .floating-container-rsr:hover {{ right: 0; }}
        .rsr-tab {{
            position: absolute; left: -40px; top: 0; background: #1b263b;
            width: 40px; height: 50px; display: flex; align-items: center;
            justify-content: center; border-radius: 10px 0 0 10px; cursor: pointer; font-size: 20px;
        }}
        .floating-container-rsr a {{
            color: #a3b18a !important; display: block; margin: 12px 0;
            text-decoration: none !important; font-size: 13px; font-weight: bold;
        }}
        .floating-container-rsr a:hover {{ color: white !important; }}
        </style>

        <div class="floating-container-rsr">
            <div class="rsr-tab">🛠️</div>
            <p style="margin:0; font-size:14px; font-weight:bold; text-align:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:5px;">Herramientas</p>
            <a href="{link_pdf}" download="Manual_Operacion_RSR.pdf">📂 Descargar Manual</a>
            <a href="https://www.imss.gob.mx/" target="_blank">🏥 Portal IMSS</a>
            <a href="https://wa.me/tu_numero" target="_blank">👨‍💻 Soporte TICs</a>
        </div>
    """, unsafe_allow_html=True)

# --- 5. BARRA LATERAL (TU SIDEBAR ORIGINAL) ---
with st.sidebar:
    logo_b64 = get_base64_image("Imagenes/SR.png")
    if logo_b64:
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_b64}" width="150"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Bienvenido</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a3b18a;'>Rancho Santa Rosa</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    
    if "nombre_fijado" not in st.session_state:
        st.session_state["nombre_fijado"] = False
    if "usuario_actual" not in st.session_state:
        st.session_state["usuario_actual"] = ""

    usuario_input = st.text_input(
        "👤 Identificar este equipo como:", 
        value=st.session_state["usuario_actual"],
        placeholder="Escribe tu nombre",
        disabled=st.session_state["nombre_fijado"],
        help="Una vez ingresado, no podrá ser modificado en esta sesión."
    )

    if usuario_input.strip() != "" and not st.session_state["nombre_fijado"]:
        st.session_state["usuario_actual"] = usuario_input
        st.session_state["nombre_fijado"] = True
        guardar_usuario_permanente(usuario_input) 
        st.rerun()

    st.markdown("---")
    
    if st.session_state["nombre_fijado"]:
        menu = st.radio("Seleccione una sección:", 
                        ["📄 Información", "👥 Registro de Accesos", "📕 IMSS Mensual", "📖 IMSS Bimestral", "🗓️ Procesamiento de Nomina"],
                        key="menu_principal")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col_side1, col_side2, col_side3 = st.columns([0.5, 2, 0.5])
        with col_side2:
            if st.button("🔴 Cerrar Sesión", use_container_width=True):
                st.session_state["nombre_fijado"] = False
                st.session_state["usuario_actual"] = ""
                st.rerun()
    else:
        st.warning("⚠️ Debes ingresar tu nombre para continuar.")
        menu = "🔒 Bloqueado"
    
    st.markdown('<div class="version-container">Versión 1.1.5<br>TICS & Administración</div>', unsafe_allow_html=True)

# --- 6. CABECERA: FECHA, HORA Y CLIMA ---
ahora_mx = obtener_hora_mexico()
st.markdown(f"""
    <div style="text-align: right; color: #1b263b; font-size: 1.1em; font-weight: bold; padding: 10px; margin-bottom: -15px;">
        {ahora_mx.strftime('%A, %d de %B de %Y')} | {ahora_mx.strftime('%I:%M %p')} | {obtener_clima_ficticio()}
    </div>
""", unsafe_allow_html=True)

# --- 7. NAVEGACIÓN (TU LÓGICA ORIGINAL) ---

if menu == "🔒 Bloqueado":
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_bloqueo, _ = st.columns([1, 2, 1])
    with col_bloqueo:
        st.info("### 👋 Identificación Requerida")
        st.write("Para habilitar las herramientas de administración, ingresa tu nombre completo en el panel izquierdo.")

elif menu == "📄 Información":
    if "historial_procesos" not in st.session_state:
        st.session_state["historial_procesos"] = []
        
    _, col_centro, _ = st.columns([1, 2, 1])
    with col_centro:
        img_control_b64 = get_base64_image("Imagenes/control.png")
        if img_control_b64:
            st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_control_b64}" width="150"></div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>Gestión de Contador</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:gray;'>Última actualización global: {leer_ultima_fecha()}</p>", unsafe_allow_html=True)

    st.divider()

    # MÉTRICAS ORIGINALES
    so_v, pc_v, _ = obtener_info_sistema()
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown(f"""<div class="metric-card">
            <p style='color:gray; font-size: 0.9em;'>SISTEMA EN NUBE</p>
            <h2 style='color:#1b263b; margin:0;'>{so_v}</h2>
            <small style='color:gray;'>Sesión iniciada por: <b>{st.session_state["usuario_actual"]}</b></small>
        </div>""", unsafe_allow_html=True)
        
    with col_b:
        st.markdown(f"""<div class="metric-card">
            <p style='color:gray; font-size: 0.9em;'>CONEXIÓN DE RED</p>
            <h2 style='color:#1b263b; margin:0;'>{verificar_conexion_internet()}</h2>
        </div>""", unsafe_allow_html=True)

    with col_c:
        total_hoy = len(st.session_state.get("historial_procesos", []))
        color_num = "#2e7d32" if total_hoy > 0 else "#1b263b"
        st.markdown(f"""<div class="metric-card">
            <p style='color:gray; font-size: 0.9em;'>PROCESOS HOY</p>
            <h2 style='color:{color_num}; margin:0; font-size: 48px;'>{total_hoy}</h2>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align: center;'>🕒 Actividad Reciente</h3>", unsafe_allow_html=True)
    
    if st.session_state.get("historial_procesos"):
        for item in reversed(st.session_state["historial_procesos"]):
            st.markdown(f"""<div style="background:white; padding:10px; border-radius:8px; margin-bottom:5px; border-left:5px solid #1b263b; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">{item['tipo']} | <b>Archivo:</b> {item['archivo']} | <span style="color:#1b263b;">💻 {item.get('equipo', 'PC')}</span> | {item['hora']}</div>""", unsafe_allow_html=True)
    else:
        st.info("No se han registrado movimientos en la sesión actual.")

elif menu == "👥 Registro de Accesos":
    mostrar_interfaz_registro()
elif menu == "📕 IMSS Mensual":
    mostrar_interfaz_imssme()
elif menu == "📖 IMSS Bimestral":
    mostrar_interfaz_imssbi()
elif menu == "🗓️ Procesamiento de Nomina":
    mostrar_interfaz_nomina_azu()
