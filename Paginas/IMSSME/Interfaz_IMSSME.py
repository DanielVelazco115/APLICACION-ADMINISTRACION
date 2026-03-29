import streamlit as st
import os
import tempfile
import unicodedata
import pandas as pd # Agregamos pandas para la validación
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

        # 2. ENCABEZADO CENTRADO
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Administración</h2>", unsafe_allow_html=True)
    st.divider()

    # --- LÓGICA INTERNA (Funciones de apoyo) ---
    def normalizar_nombre(nombre):
        if not nombre:
            return "SIN DEPTO"
        nombre = nombre.upper()
        nombre = "".join(
            c for c in unicodedata.normalize("NFD", nombre)
            if unicodedata.category(c) != "Mn"
        )
        return " ".join(nombre.split())

    def pintar_encabezados(hoja):
        verde = PatternFill(start_color="CCFFCC", end_color="CCFFCC", fill_type="solid")
        rosa = PatternFill(start_color="FFCCFF", end_color="FFCCFF", fill_type="solid")
        azul = PatternFill(start_color="66CCFF", end_color="66CCFF", fill_type="solid")
        for col in range(1, 10):
            hoja.cell(row=1, column=col).fill = verde
        for col in [10,11,13,15,17,18,20]:
            hoja.cell(row=1, column=col).fill = rosa
        for col in [12,14,16,19]:
            hoja.cell(row=1, column=col).fill = azul

    # 2. ÁREA DE CARGA DE ARCHIVOS
    st.subheader("Paso 1: Sube tus archivos")
    
    archivo_principal = st.file_uploader("Sube el archivo plantilla IMSS mensual.xlsx (EMA)", type=["xlsx"])
    archivo_nombres = st.file_uploader("Sube el archivo nombres organizados.xlsx (Catálogo)", type=["xlsx"])

    st.info("ℹ️ Asegúrate de subir ambos archivos para comenzar.")

    # 3. PROCESAMIENTO
    st.subheader("Estado del Proceso")
    if archivo_principal and archivo_nombres:
        
        # --- VALIDACIÓN DE FILAS 6 EN ADELANTE (EMA MENSUAL) ---
        try:
            xls = pd.ExcelFile(archivo_principal)
            # Buscamos la hoja EMA (o la primera disponible si no se llama así)
            hojas_validar = [h for h in xls.sheet_names if "EMA" in h.upper()]
            
            # Si no hay una hoja con nombre EMA, revisamos la primera hoja del libro
            if not hojas_validar:
                hojas_validar = [xls.sheet_names[0]]

            datos_encontrados = False
            for hoja in hojas_validar:
                # Leemos saltando las primeras 5 filas (empieza en la 6)
                df_temp = pd.read_excel(xls, sheet_name=hoja, skiprows=5)
                # Limpiamos nulos para ver si hay contenido real
                if not df_temp.dropna(how='all').empty:
                    datos_encontrados = True
                    break
            
            if not datos_encontrados:
                st.error(f"❌ ERROR: El archivo '{archivo_principal.name}' no tiene trabajadores registrados.")
                st.warning("No se detectaron datos a partir de la fila 6 en adelante.")
                st.stop() # Bloqueo inmediato
                
        except Exception as e:
            st.error(f"❌ Error al validar el contenido mensual: {e}")
            st.stop()
        # --- FIN DE VALIDACIÓN ---

        st.success("✅ Archivos listos para procesar.")
        
        # Guardar temporalmente
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
                    # Llamamos a la función consolidar
                    ruta_salida = revision.consolidar(ruta_principal, ruta_nombres, carpeta_temp)
                    
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
