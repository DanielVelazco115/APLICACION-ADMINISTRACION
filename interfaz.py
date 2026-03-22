import streamlit as st
import os
import tempfile
import revision

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Pestaña)
# ==========================================
st.set_page_config(
    page_title="Consolidación IMSS", 
    page_icon="📊",  # Puedes cambiar este emoji por la ruta de un icono png
    layout="wide"     # 'centered' para más estrecho, 'wide' para ocupar toda la pantalla
)
# ==========================================
# 2. ENCABEZADO Y LOGO
# ==========================================
# Creamos dos columnas para el encabezado
col_logo, col_titulo = st.columns([1, 5]) # Proporción 1 a 5

with col_logo:
    # --- ¡IMPORTANTE! ---
    # Reemplaza 'ruta/a/tu/logo.png' por la ruta real de tu archivo de imagen
    # o usa una URL directa (como el ejemplo de abajo).
    # Mientras tanto, usaré una imagen de ejemplo de un gráfico.
    st.image("imagenes/SR.png", width=180) 

with col_titulo:
    # Título principal con un toque de HTML para el color (puedes cambiar #004691)
    st.markdown("<h1 style='color: #004691; margin-top: -10px;'>Revision del EMA & EBA Bimestral</h1>", unsafe_allow_html=True)
    st.write("Bienvenido, Utiliza el menú lateral para subir tus archivos.")

st.divider() # Línea divisoria visual

# ==========================================
# 3. --- ENCABEZADO CENTRADO ---
# ==========================================

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Centramos el logo
    #st.image("SR.png", use_container_width=True)u
    # Centramos el título con HTML
    st.markdown("<h2 style='text-align: center;'>Administración/ Rancho Santa Rosa</h2>", unsafe_allow_html=True)
    #st.image("SR.png", width=180)

st.divider()

# --- ÁREA DE CARGA (Ahora en el centro) ---
st.subheader("Paso 1: Sube tus archivos")

# Creamos dos columnas para que los cargadores salgan uno al lado del otro
# O déjalos sueltos para que salgan uno arriba del otro (más cómodo en celular)
archivo_principal = st.file_uploader("Sube plantilla IMSS bimestral", type=["xlsx"])
archivo_nombres = st.file_uploader("Sube nombres organizados", type=["xlsx"])

st.info("ℹ️ Asegúrate de que ambos archivos estén cargados antes de procesar.")

# ==========================================
# 4. ÁREA PRINCIPAL - Lógica y Salidas
# ==========================================

st.subheader("Estado del Proceso")

# Verificamos si ambos archivos han sido subidos
if archivo_principal and archivo_nombres:
    
    # Mostramos un mensaje visual de "Archivos Listos"
    st.success("✅ ¡Archivos cargados correctamente!")
    st.markdown("---") # Separador

    # Creamos dos columnas para mostrar un resumen de lo cargado
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Plantilla:** `{archivo_principal.name}`")
    with col2:
        st.write(f"**Nombres:** `{archivo_nombres.name}`")

    # Lógica de guardado temporal (original de tu código)
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
        # El botón nativo ya toma color si configuras un tema más adelante
        btn_procesar = st.button("🚀 Iniciar Procesamiento")

    if btn_procesar:
        # Usamos un 'spinner' (animación de carga) para que se vea profesional
        with st.spinner('Consolidando datos... por favor espera.'):
            try:
                # Tu lógica de negocio
                ruta_salida = revision.consolidar(ruta_principal, ruta_nombres, carpeta_temp)
                
                # ¡Éxito! Efecto visual de globos y mensaje verde
                st.balloons() 
                st.success("🎉 ¡Consolidación exitosa! Tu archivo está listo.")
                
                # Botón de descarga más llamativo
                with open(ruta_salida, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar archivo consolidado (Excel)",
                        data=f,
                        file_name=os.path.name(ruta_salida),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True # Que ocupe todo el ancho de su columna
                    )
                    
            except Exception as e:
                # Usamos el contenedor de error nativo (rojo)
                st.error(f"❌ Ocurrió un error inesperado durante el proceso:\n\n`{e}`")

else:
    # Mensaje cuando aún no se suben los archivos
    st.warning("⚠️ Esperando que subas ambos archivos Excel en la barra lateral izquierda...")
    
    # Podemos poner una imagen o icono grande de espera
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; opacity: 0.5;'>
        <img src='https://cdn-icons-png.flaticon.com/512/3342/3342137.png' width='150'>
        <p>Sube tus archivos para comenzar</p>
    </div>
    """, unsafe_allow_html=True)
