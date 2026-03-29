import streamlit as st
import pandas as pd
import os
from datetime import datetime
# Importaciones actualizadas para tu nueva estructura
from Paginas.IMSSBI.Interfaz_IMSSBI import mostrar_interfaz_imssbi
from Paginas.IMSSME.Interfaz_IMSSME import mostrar_interfaz_imssme
from Paginas.NOMINA.Interfaz_Nomina_Azu import mostrar_interfaz_nomina_azu
# --- FUNCIONES DE MEMORIA AUTOMÁTICA ---
FECHA_LOG = "fecha_modificacion.txt"

def actualizar_fecha_servidor():
    # Obtiene fecha actual. Ejemplo: 23 de Marzo, 2026 a las 15:30
    ahora = datetime.now().strftime("%d de %B, %Y a las %H:%M")
    with open(FECHA_LOG, "w") as f:
        f.write(ahora)
    return ahora

def leer_ultima_fecha():
    if os.path.exists(FECHA_LOG):
        with open(FECHA_LOG, "r") as f:
            return f.read()
    return "15 de Octubre" # Fecha por defecto inicial

# Inyectar CSS para centrar los elementos del radio button en la sidebar
st.markdown("""
    <style>
    /* Centra el contenedor del radio button */
    [data-testid="stSidebarNav"] {
        text-align: center;
    }
    
    /* Centra el texto de las opciones del radio */
    div[data-testid="stRadio"] > label {
        display: flex;
        justify-content: center;
        font-weight: bold;
    }

    /* Centra las opciones individuales */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Configuración de la página (Debe ser lo primero)
st.set_page_config(
    page_title="Admin Pro Panel",
    page_icon="🏢",
    layout="wide", # Usa todo el ancho de la pantalla
    initial_sidebar_state="expanded"
)

# 2. Estilo CSS Personalizado para "tunear" los contenedores
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background-color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Barra Lateral (Sidebar) con estilo
with st.sidebar:
    # 1. Imagen centrada (usando columnas)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("Imagenes/SR.png", use_container_width=True)

    # 2. Títulos centrados (usando el parámetro nativo)
    st.title("Bienvenido", text_alignment="center")
    st.subheader("Rancho Santa Rosa", text_alignment="center", help="Panel de administración") # Subheader se ve más elegante

    st.markdown("---")

    # 3. El Menú Radio (Ahora se verá centrado por el CSS de arriba)
    menu = st.sidebar.radio(
        "¿Qué Sección Buscas?", 
        ["📄 Informacion", "📕 IMSS Mensual", "📖 IMSS Bimestral", "🗓️ NOMINA & AZU"],
        #label_visibility="visible" # Puedes usar "collapsed" si quieres que el título no estorbe
    )

    st.markdown("---")
    st.info("Versión 1.0.2")

    # --- 4. Cuerpo Principal ---
if menu == "📄 Informacion":
    # ESTO ES LO ÚNICO QUE DEBE VERSE EN INFORMACIÓN
    fecha_mostrar = leer_ultima_fecha()
    st.info(f"Último reporte cargado: {fecha_mostrar}")
    st.title("🚀 Panel de Control Administrativo")
    st.markdown("---")
    st.subheader("Bienvenido al sistema de gestión de Rancho Santa Rosa.")
    st.write("Selecciona una opción en el menú de la izquierda para comenzar.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Estado del sistema:** Operativo")
    with col2:
        st.success("**Servidor:** Conectado")

elif menu == "📕 IMSS Mensual":
    mostrar_interfaz_imssme()

elif menu == "📖 IMSS Bimestral": # Asegúrate que este emoji coincida con el de la línea 92
    mostrar_interfaz_imssbi()

elif menu == "🗓️ NOMINA & AZU":
    mostrar_interfaz_nomina_azu()

