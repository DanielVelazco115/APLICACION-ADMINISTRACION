import streamlit as st
import os
import tempfile
import revision

st.title("Consolidación IMSS")

archivo_principal = st.file_uploader("Sube plantilla IMSS bimestral", type=["xlsx"])
archivo_nombres = st.file_uploader("Sube nombres organizados", type=["xlsx"])

if archivo_principal and archivo_nombres:
    carpeta_temp = tempfile.mkdtemp()
    ruta_principal = os.path.join(carpeta_temp, archivo_principal.name)
    ruta_nombres = os.path.join(carpeta_temp, archivo_nombres.name)

    with open(ruta_principal, "wb") as f:
        f.write(archivo_principal.getbuffer())
    with open(ruta_nombres, "wb") as f:
        f.write(archivo_nombres.getbuffer())

    if st.button("Procesar"):
        try:
            ruta_salida = revision.consolidar(ruta_principal, ruta_nombres, carpeta_temp)
            with open(ruta_salida, "rb") as f:
                st.download_button(
                    label="Descargar archivo consolidado",
                    data=f,
                    file_name=os.path.basename(ruta_salida),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Error: {e}")
