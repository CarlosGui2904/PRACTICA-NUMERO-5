import streamlit as st

from modulos.login import login
from modulos.ventas import mostrar_venta
from modulos.pacientes import mostrar_pacientes


# Inicializar variables de sesión
if "sesion_iniciada" not in st.session_state:
    st.session_state["sesion_iniciada"] = False

if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""


# Comprobar si el usuario inició sesión
if st.session_state["sesion_iniciada"]:

    # Menú lateral
    st.sidebar.title("Menú principal")

    st.sidebar.write(
        f"Usuario: {st.session_state['usuario']}"
    )

    opciones = [
        "Ventas",
        "Pacientes",
        "Información"
    ]

    seleccion = st.sidebar.selectbox(
        "Seleccione una opción",
        opciones
    )

    # Módulo de ventas
    if seleccion == "Ventas":
        mostrar_venta()

    # Módulo de pacientes
    elif seleccion == "Pacientes":
        mostrar_pacientes()

    # Módulo de información
    elif seleccion == "Información":
        st.header("Información del sistema")

        st.write(
            "Sistema de gestión de información "
            "para una clínica."
        )

        st.write(
            "Esta aplicación permite gestionar "
            "las ventas y la información administrativa "
            "de los pacientes."
        )

    # Cerrar sesión
    if st.sidebar.button("Cerrar sesión"):

        st.session_state["sesion_iniciada"] = False
        st.session_state["usuario"] = ""

        st.rerun()

else:

    # Mostrar inicio de sesión
    login()
