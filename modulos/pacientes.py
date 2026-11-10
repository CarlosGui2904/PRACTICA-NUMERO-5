import streamlit as st
from config.conexion import obtener_conexion


def mostrar_pacientes():
    st.header("Gestión de pacientes")

    # Opciones del módulo
    opcion = st.selectbox(
        "Seleccione una opción",
        [
            "Registrar paciente",
            "Consultar pacientes",
            "Buscar paciente"
        ]
    )

    # REGISTRAR PACIENTE
    if opcion == "Registrar paciente":

        st.subheader("Registro de nuevo paciente")

        with st.form("form_paciente"):

            nombre = st.text_input("Nombre completo")
            dui = st.text_input("DUI")
            telefono = st.text_input("Teléfono")

            fecha_nacimiento = st.date_input(
                "Fecha de nacimiento",
                min_value=__import__("datetime").date(1900, 1, 1)
            )

            sexo = st.selectbox(
                "Sexo",
                ["Masculino", "Femenino", "Otro"]
            )

            direccion = st.text_input("Dirección")
            correo = st.text_input("Correo electrónico")

            guardar = st.form_submit_button(
                "Guardar paciente"
            )

        if guardar:

            if nombre.strip() == "" or dui.strip() == "":
                st.warning(
                    "El nombre y el DUI son obligatorios."
                )

            else:
                conexion = None
                cursor = None

                try:
                    conexion = obtener_conexion()

                    if conexion is None:
                        return

                    cursor = conexion.cursor()

                    consulta = """
                        INSERT INTO PACIENTES
                        (Nombre, DUI, Telefono,
                        Fecha_Nacimiento, Sexo,
                        Direccion, Correo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                    cursor.execute(
                        consulta,
                        (
                            nombre.strip(),
                            dui.strip(),
                            telefono.strip(),
                            fecha_nacimiento,
                            sexo,
                            direccion.strip(),
                            correo.strip()
                        )
                    )

                    conexion.commit()

                    st.success(
                        "Paciente registrado correctamente."
                    )

                except Exception as error:

                    if conexion is not None:
                        conexion.rollback()

                    if "Duplicate entry" in str(error):
                        st.error(
                            "Ya existe un paciente registrado con ese DUI."
                        )
                    else:
                        st.error(
                            f"Error al registrar paciente: {error}"
                        )

                finally:

                    if cursor is not None:
                        cursor.close()

                    if (
                        conexion is not None
                        and conexion.is_connected()
                    ):
                        conexion.close()

    # CONSULTAR PACIENTES
    elif opcion == "Consultar pacientes":

        st.subheader("Listado de pacientes")

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return

            cursor = conexion.cursor()

            consulta = """
                SELECT Id_Paciente, Nombre, DUI,
                       Telefono, Fecha_Nacimiento,
                       Sexo, Direccion, Correo
                FROM PACIENTES
                ORDER BY Id_Paciente DESC
            """

            cursor.execute(consulta)

            resultados = cursor.fetchall()

            if resultados:

                columnas = [
                    "ID",
                    "Nombre",
                    "DUI",
                    "Teléfono",
                    "Fecha de nacimiento",
                    "Sexo",
                    "Dirección",
                    "Correo"
                ]

                st.dataframe(
                    resultados,
                    column_config={
                        "ID": st.column_config.NumberColumn("ID"),
                    },
                    use_container_width=True
                )

                st.caption(
                    f"Total de pacientes registrados: {len(resultados)}"
                )

            else:
                st.info(
                    "Todavía no hay pacientes registrados."
                )

        except Exception as error:
            st.error(
                f"Error al consultar pacientes: {error}"
            )

        finally:

            if cursor is not None:
                cursor.close()

            if (
                conexion is not None
                and conexion.is_connected()
            ):
                conexion.close()

    # BUSCAR PACIENTES
    elif opcion == "Buscar paciente":

        st.subheader("Buscar paciente")

        busqueda = st.text_input(
            "Ingrese el nombre o DUI del paciente"
        )

        if busqueda.strip():

            conexion = None
            cursor = None

            try:
                conexion = obtener_conexion()

                if conexion is None:
                    return

                cursor = conexion.cursor()

                consulta = """
                    SELECT Id_Paciente, Nombre, DUI,
                           Telefono, Fecha_Nacimiento,
                           Sexo, Direccion, Correo
                    FROM PACIENTES
                    WHERE Nombre LIKE %s OR DUI LIKE %s
                """

                criterio = "%" + busqueda.strip() + "%"

                cursor.execute(
                    consulta,
                    (criterio, criterio)
                )

                resultados = cursor.fetchall()

                if resultados:

                    st.write(
                        f"Se encontraron {len(resultados)} resultado(s)."
                    )

                    st.dataframe(
                        resultados,
                        use_container_width=True
                    )

                else:
                    st.warning(
                        "No se encontraron pacientes."
                    )

            except Exception as error:
                st.error(
                    f"Error al buscar pacientes: {error}"
                )

            finally:

                if cursor is not None:
                    cursor.close()

                if (
                    conexion is not None
                    and conexion.is_connected()
                ):
                    conexion.close()
