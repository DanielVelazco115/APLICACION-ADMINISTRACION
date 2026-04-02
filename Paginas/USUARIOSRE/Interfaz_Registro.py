import streamlit as st
import os

LOG_USUARIOS = "registro_usuarios.txt"

def leer_usuarios_registrados():
    if os.path.exists(LOG_USUARIOS):
        with open(LOG_USUARIOS, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

def mostrar_interfaz_registro():
    st.markdown("<h1 style='text-align: center; color: #1b263b;'>👥 Registro Histórico de Accesos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d;'>Listado permanente de personal que ha ingresado al sistema.</p>", unsafe_allow_html=True)
    st.divider()

    usuarios = leer_usuarios_registrados()

    if usuarios:
        # Buscador simple por si la lista crece mucho
        busqueda = st.text_input("🔍 Buscar usuario...", placeholder="Escribe un nombre...")
        
        st.markdown("---")
        
        # Mostramos los registros (del más reciente al más antiguo)
        for u in reversed(usuarios):
            if "|" in u:
                fecha, nombre = u.split(" | ")
                if busqueda.lower() in nombre.lower():
                    st.markdown(f"""
                    <div style="background-color: white; padding: 15px; border-radius: 10px; 
                                border-left: 5px solid #a3b18a; margin-bottom: 10px; 
                                box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <span style="color: #888; font-size: 0.85em;">📅 {fecha}</span><br>
                        <strong style="color: #0d1b2a; font-size: 1.1em;">👤 {nombre.strip()}</strong>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Aún no hay usuarios registrados en la base de datos local.")