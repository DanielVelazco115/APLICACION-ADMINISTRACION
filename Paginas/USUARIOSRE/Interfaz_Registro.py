import streamlit as st
import os

LOG_USUARIOS = "registro_usuarios.txt"
LOG_ACTIVIDAD = "log_actividad.txt" # <-- Nueva fuente de datos

def leer_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

def mostrar_interfaz_registro():
    st.markdown("<h1 style='text-align: center; color: #1b263b;'>👥 Registro Histórico de Actividad</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6c757d;'>Monitoreo permanente de accesos y acciones realizadas en el sistema.</p>", unsafe_allow_html=True)
    st.divider()

    # PESTAÑAS PARA ORGANIZAR LA INFORMACIÓN
    tab1, tab2 = st.tabs(["🕒 Actividad Detallada", "👤 Inicios de Sesión"])

    with tab1:
        st.subheader("Acciones en el Sistema")
        actividades = leer_datos(LOG_ACTIVIDAD)
        
        if actividades:
            busqueda_act = st.text_input("🔍 Filtrar por acción o usuario...", placeholder="Ej: Daniel o Procesó...", key="bus_act")
            st.markdown("---")
            
            for line in reversed(actividades):
                if "|" in line:
                    # Formato esperado: Fecha | USUARIO: X | ACCIÓN: Y | DETALLE: Z
                    partes = line.split(" | ")
                    fecha = partes[0]
                    usuario = partes[1].replace("USUARIO: ", "")
                    accion = partes[2].replace("ACCIÓN: ", "")
                    detalle = partes[3].replace("DETALLE: ", "") if len(partes) > 3 else ""

                    if busqueda_act.lower() in line.lower():
                        # Color dinámico según la acción
                        color_borde = "#2a9d8f" if "COMPLETADO" in accion else "#e76f51" if "ERROR" in accion else "#1b263b"
                        
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 10px; 
                                    border-left: 5px solid {color_borde}; margin-bottom: 10px; 
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: #888; font-size: 0.85em;">📅 {fecha}</span>
                                <span style="background-color: #f1f3f5; padding: 2px 8px; border-radius: 5px; font-size: 0.75em; font-weight: bold;">{accion}</span>
                            </div>
                            <strong style="color: #0d1b2a;">👤 {usuario.strip()}</strong><br>
                            <span style="color: #4a4a4a; font-size: 0.9em;">📝 {detalle.strip()}</span>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("No hay acciones registradas todavía.")

    with tab2:
        st.subheader("Historial de Entradas")
        usuarios = leer_datos(LOG_USUARIOS)

        if usuarios:
            busqueda_acc = st.text_input("🔍 Buscar por nombre...", placeholder="Escribe un nombre...", key="bus_acc")
            st.markdown("---")
            
            for u in reversed(usuarios):
                if "|" in u:
                    fecha, nombre = u.split(" | ")
                    if busqueda_acc.lower() in nombre.lower():
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
