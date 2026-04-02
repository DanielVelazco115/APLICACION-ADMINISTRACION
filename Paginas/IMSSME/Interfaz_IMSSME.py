import streamlit as st
import os
import tempfile
import unicodedata
import pandas as pd
from datetime import datetime # Importante para la hora del registro
from collections import defaultdict
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill
from . import revision

def mostrar_interfaz_imssme():
    # 1. ENCABEZADO Y LOGO
    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        st.image("Paginas/IMSSME/calendario.png", width=150) 
    with col_titulo:
        st.markdown("<h1 style='color: #004691; margin-top: -10px;'>SISTEMA DE REVISION MENSUAL</h1>", unsafe_allow_html=True)
        st.write("Bienvenido, Sube tus archivos.")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Administración</h2>", unsafe_allow_html=True)
    st.divider()

    # --- LÓGICA INTERNA ---
    def normalizar_nombre(nombre):
        if not nombre: return "SIN DEPTO"
        nombre = nombre.upper()
        nombre = "".join(c for c in unicodedata.normalize("NFD", nombre) if unicodedata.category(c) != "Mn")
        return " ".join(nombre.split())

    # 2. ÁREA DE CARGA DE ARCHIVOS
    st.subheader("Paso 1: Sube tus archivos")
    
    archivo_principal = st.file_uploader("Sube el archivo plantilla IMSS mensual.xlsx (EMA)", type=["xlsx"])
    archivo_nombres = st.file_uploader("Sube el archivo nombres organizados.xlsx (Catálogo)", type=["xlsx"])

    st.info("ℹ️ Asegúrate de subir ambos archivos para comenzar.")

    # 3. PROCESAMIENTO
    st.subheader("Estado del Proceso")
    if archivo_principal and archivo_nombres:
        
        # --- VALIDACIÓN DE CONTENIDO ---
        try:
            xls = pd.ExcelFile(archivo_principal)
            hojas_validar = [h for h in xls.sheet_names if "EMA" in h.upper()]
            if not hojas_validar: hojas_validar = [xls.sheet_names[0]]

            datos_encontrados = False
            for hoja in hojas_validar:
                df_temp = pd.read_excel(xls, sheet_name=hoja, skiprows=5)
                if not df_temp.dropna(how='all').empty:
                    datos_encontrados = True
                    break
            
            if not datos_encontrados:
                st.error(f"❌ ERROR: El archivo '{archivo_principal.name}' no tiene trabajadores registrados.")
                st.stop() # Aquí se detiene y NO suma al contador
                
        except Exception as e:
            st.error(f"❌ Error al validar el contenido mensual: {e}")
            st.stop()

        st.success("✅ Archivos listos para procesar.")
        
        carpeta_temp = tempfile.mkdtemp()
        ruta_principal = os.path.join(carpeta_temp, archivo_principal.name)
        ruta_nombres = os.path.join(carpeta_temp, archivo_nombres.name)

        with open(ruta_principal, "wb") as f:
            f.write(archivo_principal.getbuffer())
        with open(ruta_nombres, "wb") as f:
            f.write(archivo_nombres.getbuffer())

        # Botón para iniciar
        if st.button("🚀 Iniciar Procesamiento Mensual"):
            with st.spinner('Procesando datos mensuales...'):
                try:
                    # Se ejecuta el proceso real
                    ruta_salida = revision.consolidar(ruta_principal, ruta_nombres, carpeta_temp)
                    
                    # --- BLOQUE DE REGISTRO PARA LA PÁGINA PRINCIPAL ---
                    # Solo llegamos aquí si 'consolidar' no falló
                    if "historial_procesos" in st.session_state:
                        nuevo_registro = {
                            "tipo": "📕 IMSS Mensual",
                            "archivo": f"{archivo_principal.name} (Procesado)",
                            "hora": datetime.now().strftime("%I:%M %p")
                        }
                        st.session_state["historial_procesos"].append(nuevo_registro)
                    # --------------------------------------------------

                    st.balloons()
                    st.success("🎉 ¡Revisión mensual terminada!")
                    
                    with open(ruta_salida, "rb") as f:
                        st.download_button(
                            label="⬇️ Descargar Excel Mensual",
                            data=f,
                            file_name=os.path.basename(ruta_salida),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Error al procesar: {e}")
    else:
        st.warning("⚠️ Esperando que subas ambos archivos Excel...")
