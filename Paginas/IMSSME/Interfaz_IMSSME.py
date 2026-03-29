import streamlit as st
import os
import tempfile
import unicodedata
from collections import defaultdict
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, PatternFill
from . import revision

def mostrar_interfaz_imssme():
    # 1. ENCABEZADO
    st.image("Paginas/IMSSME/SR.png", width=120) 
    st.title("SISTEMA DE REVISIÓN IMSS MENSUAL")
    st.write("---")

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
    st.subheader("Paso 1: Sube tus archivos mensuales")
    
    archivo_principal = st.file_uploader("Sube plantilla IMSS mensual (EMA)", type=["xlsx"])
    archivo_nombres = st.file_uploader("Sube nombres organizados (Catálogo)", type=["xlsx"])

    st.info("ℹ️ Asegúrate de subir ambos archivos para comenzar.")

    # 3. PROCESAMIENTO
    if archivo_principal and archivo_nombres:
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
                    # Llamamos a la función consolidar que está dentro de revision.py (mismo de la carpeta)
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
        st.warning("⚠️ Esperando archivos...")