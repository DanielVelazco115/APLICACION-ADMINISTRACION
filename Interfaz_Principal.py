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
    ahora = datetime.now().strftime("%d de %B, %Y a las %H:%M")
    with open(FECHA_LOG, "w") as f:
        f.write(ahora)
    return ahora

def leer_ultima_fecha():
    if os.path.exists(FECHA_LOG):
        with open(FECHA_LOG, "r") as f:
            return f.read()
    return "Sin registros previos"

# --- INICIALIZAR MEMORIA DE SESIÓN (Historial) ---
if "historial_procesos" not in st.session_state:
    st.session_state["historial_procesos"] = []

# CSS para centrar y tunear la interfaz
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { text-align: center; }
    div[data-testid="stRadio"] > label { display: flex; justify-content: center; font-weight: bold; }
    div[data-testid="stRadio"] div[role="radiogroup"] { display: flex; flex-direction: column; align-items: center; }
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    /* Estilo para las tarjetas del historial */
    .historial-card {
        background-color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border-left: 5px solid #004691;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Configuración de la página
st.set_page_config(
    page_title="Admin Pro Panel",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Barra Lateral (Sidebar)
with st.sidebar:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("Imagenes/SR.png", use_container_width=True)

    st.title("Bienvenido", text_alignment="center")
    st.subheader("Rancho Santa Rosa", text_alignment="center")

    st.markdown("---")

    menu = st.sidebar.radio(
        "¿Qué Sección Buscas?", 
        ["📄 Informacion", "📕 IMSS Mensual", "📖 IMSS Bimestral", "🗓️ NOMINA & AZU"]
    )

    st.markdown("---")
    st.info("Versión 1.0.2")

# --- 3. Cuerpo Principal ---
if menu == "📄 Informacion":
    st.title("🚀 Panel de Control Administrativo")
    
    # Métricas superiores
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Estado", "Operativo ✅")
    with col_b:
        st.metric("Servidor", "Conectado 🌐")
    with col_c:
        total_hoy = len(st.session_state["historial_procesos"])
        st.metric("Procesos en sesión", total_hoy)

    st.markdown("---")

    # SECCIÓN DE MOVIMIENTOS DINÁMICOS
    st.subheader("🕒 Actividad Reciente de la Sesión")
    
    if st.session_state["historial_procesos"]:
        # Mostramos los últimos movimientos registrados
        for item in reversed(st.session_state["historial_procesos"]):
            st.markdown(f"""
            <div class="historial-card">
                <span style="color: #004691; font-weight: bold;">{item['tipo']}</span> | 
                <b>Archivo:</b> {item['archivo']} | 
                <span style="color: gray; font-size: 0.8em;">{item['hora']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("No se han realizado procesos en esta sesión todavía.")
        st.caption("Cuando proceses un archivo en IMSS o Nómina, aparecerá aquí el registro.")

    st.markdown("---")
    fecha_mostrar = leer_ultima_fecha()
    st.info(f"Última modificación global detectada: {fecha_mostrar}")

elif menu == "📕 IMSS Mensual":
    mostrar_interfaz_imssme()

elif menu == "📖 IMSS Bimestral":
    mostrar_interfaz_imssbi()

elif menu == "🗓️ NOMINA & AZU":
    mostrar_interfaz_nomina_azu()
