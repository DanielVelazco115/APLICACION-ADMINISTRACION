import streamlit as st
import os
import tempfile
import pandas as pd
from . import revision

def mostrar_interfaz_imssbi():
    # 1. ENCABEZADO Y LOGO
    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        st.image("Paginas/IMSSBI/calendario.png", width=150) 
    with col_titulo:
        st.markdown("<h1 style='color: #004691; margin-top: -10px;'>SISTEMA DE REVISION BIMESTRAL</h1>", unsafe_allow_html=True)
        st.write("Bienvenido, Sube tus archivos.")

    st.divider()

    # 2. ENCABEZADO CENTRADO
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Administración</h2>", unsafe_allow_html=True)

    st.divider()

    # 3. ÁREA DE CARGA
    st.subheader("Paso 1: Sube tus archivos")
    archivo_principal = st.file_uploader("Sube el archivo plantilla IMSS bimestral.xlsx", type=["xlsx"])
    archivo_nombres = st.file_uploader("Sube nombres el archivo organizados.xlsx", type=["xlsx"])

    st.info("ℹ️ Asegúrate de que ambos archivos estén cargados antes de procesar.")

    # 4. ÁREA PRINCIPAL
    st.subheader("Estado del Proceso")

    if archivo_principal and archivo_nombres:
        
        # --- VALIDACIÓN DE FILAS 6 EN ADELANTE EN EMA Y EBA ---
        try:
            xls = pd.ExcelFile(archivo_principal)
            hojas_disponibles = [h for h in xls.sheet_names if h.upper() in ["EMA", "EBA"]]
            
            if not hojas_disponibles:
                st.error("❌ El archivo no contiene las hojas 'EMA' o 'EBA'.")
                st.stop()

            datos_encontrados = False
            
            for hoja in hojas_disponibles:
                # Saltamos las primeras 5 filas (skiprows=5 lee desde la 6 en adelante)
                df_temp = pd.read_excel(xls, sheet_name=hoja, skiprows=5)
                
                # Limpiamos filas completamente vacías
                df_limpio = df_temp.dropna(how='all')
                
                if not df_limpio.empty:
                    datos_encontrados = True
                    break # Si encontramos datos en una, es suficiente para continuar

            if not datos_encontrados:
                st.error("❌ ERROR: No se detectaron datos de trabajadores en las hojas EMA/EBA.")
                st.warning("Las hojas están vacías desde la fila 6 en adelante. Por favor, revisa tu archivo.")
                st.stop() # Bloqueo total: No aparece botón de procesar ni descargar

        except Exception as e:
            st.error(f"❌ Error técnico al validar filas: {e}")
            st.stop()
        # --- FIN DE VALIDACIÓN ---

        st.success("✅ ¡Archivos validados con datos detectados!")
        st.markdown("---")

        # Preparación de archivos para procesamiento
        carpeta_temp = tempfile.mkdtemp()
        ruta_principal = os.path.join(carpeta_temp, archivo_principal.name)
        ruta_nombres = os.path.join(carpeta_temp, archivo_nombres.name)

        with open(ruta_principal, "wb") as f:
            f.write(archivo_principal.getbuffer())
        with open(ruta_nombres, "wb") as f:
            f.write(archivo_nombres.getbuffer())

        # Botón de Procesar
        left_spacer, center_button, right_spacer = st.columns([2, 1, 2])
        with center_button:
            btn_procesar = st.button("🚀 Iniciar Procesamiento")

        if btn_procesar:
            with st.spinner('Consolidando datos...'):
                try:
                    ruta_salida = revision.consolidar(ruta_principal, ruta_nombres, carpeta_temp)
                    
                    st.balloons() 
                    st.success("🎉 ¡Consolidación exitosa!")
                    
                    with open(ruta_salida, "rb") as f:
                        st.download_button(
                            label="⬇️ Descargar archivo consolidado (Excel)",
                            data=f,
                            file_name=os.path.basename(ruta_salida),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"❌ Error durante el proceso: `{e}`")

    else:
        st.warning("⚠️ Esperando que subas ambos archivos Excel...")
