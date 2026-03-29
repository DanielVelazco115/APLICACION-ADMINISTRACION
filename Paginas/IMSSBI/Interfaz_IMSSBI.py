import streamlit as st
import os
import tempfile
from . import revision

def mostrar_interfaz_imssbi():
    # --- TODO ESTE BLOQUE AHORA TIENE TAB (Sangría) ---
    
    # 1. ENCABEZADO Y LOGO
    # Creamos dos columnas para el encabezado
    col_logo, col_titulo = st.columns([1, 5]) # Proporción 1 a 5

    with col_logo:
        # Ruta corregida para la nueva estructura de carpetas
        st.image("Paginas/IMSSBI/SR.png", width=180) 

    with col_titulo:
        # Título principal con HTML
        st.markdown("<h1 style='color: #004691; margin-top: -10px;'>Revision del EMA & EBA Bimestral</h1>", unsafe_allow_html=True)
        st.write("Bienvenido, Sube tus archivos.")

    st.divider() # Línea divisoria visual

    # 2. ENCABEZADO CENTRADO
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h2 style='text-align: center;'>Administración/ Rancho Santa Rosa</h2>", unsafe_allow_html=True)

    st.divider()

    # 3. ÁREA DE CARGA
    st.subheader("Paso 1: Sube tus archivos")

    archivo_principal = st.file_uploader("Sube plantilla IMSS bimestral", type=["xlsx"])
    archivo_nombres = st.file_uploader("Sube nombres organizados", type=["xlsx"])

    st.info("ℹ️ Asegúrate de que ambos archivos estén cargados antes de procesar.")

    # 4. ÁREA PRINCIPAL - Lógica y Salidas
    st.subheader("Estado del Proceso")

    # Verificamos si ambos archivos han sido subidos
    if archivo_principal and archivo_nombres:
        
        # Mostramos un mensaje visual de "Archivos Listos"
        st.success("✅ ¡Archivos cargados correctamente!")
        st.markdown("---") # Separador

        # Resumen de lo cargado
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.write(f"**Plantilla:** `{archivo_principal.name}`")
        with col2_res:
            st.write(f"**Nombres:** `{archivo_nombres.name}`")

        # Lógica de guardado temporal
        carpeta_temp = tempfile.mkdtemp()
        ruta_principal = os.path.join(carpeta_temp, archivo_principal.name)
        ruta_nombres = os.path.join(carpeta_temp, archivo_nombres.name)

        with open(ruta_principal, "wb") as f:
            f.write(archivo_principal.getbuffer())
        with open(ruta_nombres, "wb") as f:
            f.write(archivo_nombres.getbuffer())

        st.markdown("---") # Separador

        # Centramos el botón de procesar
        left_spacer, center_button, right_spacer = st.columns([2, 1, 2])
        
        with center_button:
            btn_procesar = st.button("🚀 Iniciar Procesamiento")

        if btn_procesar:
            # Spinner de carga
            with st.spinner('Consolidando datos... por favor espera.'):
                try:
                    # Llamada a la lógica del archivo revision.py
                    ruta_salida = revision.consolidar(ruta_principal, ruta_nombres, carpeta_temp)
                    
                    st.balloons() 
                    st.success("🎉 ¡Consolidación exitosa! Tu archivo está listo.")
                    
                    # Botón de descarga
                    with open(ruta_salida, "rb") as f:
                        st.download_button(
                            label="⬇️ Descargar archivo consolidado (Excel)",
                            data=f,
                            file_name=os.path.basename(ruta_salida),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                        
                except Exception as e:
                    st.error(f"❌ Ocurrió un error inesperado durante el proceso:\n\n`{e}`")

    else:
        # Mensaje cuando aún no se suben los archivos
        st.warning("⚠️ Esperando que subas ambos archivos Excel...")
        
        st.markdown("""
        <div style='text-align: center; margin-top: 50px; opacity: 0.5;'>
            <img src='https://cdn-icons-png.flaticon.com/512/3342/3342137.png' width='150'>
            <p>Sube tus archivos para comenzar</p>
        </div>
        """, unsafe_allow_html=True)