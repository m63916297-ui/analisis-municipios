import streamlit as st
import pandas as pd
from datetime import datetime, time
import io

st.set_page_config(page_title="Dashboard Municipios Colombia", layout="wide")

st.title("Dashboard de Análisis - Municipios de Colombia")
st.markdown("---")

if "data" not in st.session_state:
    st.session_state.data = None

if "camera_enabled" not in st.session_state:
    st.session_state.camera_enabled = False

if "audio_enabled" not in st.session_state:
    st.session_state.audio_enabled = False

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Carga de Datos")

    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
        st.session_state.data = df
        st.success(f"Archivo cargado: {uploaded_file.name}")
        st.info(f"Total de registros: {len(df)}")
    else:
        st.warning("Por favor carga el archivo MunicipiosVeredas.csv")

    st.markdown("### Captura de Cámara")

    col_cam_btn, col_cam_status = st.columns([1, 2])

    with col_cam_btn:
        if st.button(
            "📷 Habilitar Cámara", key="btn_camera_toggle", use_container_width=True
        ):
            st.session_state.camera_enabled = not st.session_state.camera_enabled

    with col_cam_status:
        if st.session_state.camera_enabled:
            st.success("Cámara: HABILITADA")
        else:
            st.warning("Cámara: DESHABILITADA")

    if st.session_state.camera_enabled:
        camera_input = st.camera_input("Toma una foto para el análisis")
        if camera_input:
            st.image(camera_input, caption="Imagen capturada")
            st.success("Imagen procesada")
    else:
        st.info(
            "La cámara está deshabilitada. Presiona 'Habilitar Cámara' para activar."
        )

    st.markdown("### Entrada de Audio")

    col_aud_btn, col_aud_status = st.columns([1, 2])

    with col_aud_btn:
        if st.button(
            "🎤 Habilitar Audio", key="btn_audio_toggle", use_container_width=True
        ):
            st.session_state.audio_enabled = not st.session_state.audio_enabled

    with col_aud_status:
        if st.session_state.audio_enabled:
            st.success("Audio: HABILITADO")
        else:
            st.warning("Audio: DESHABILITADO")

    if st.session_state.audio_enabled:
        audio_input = st.audio_input("Graba un audio con observaciones")
        if audio_input:
            st.audio(audio_input)
            st.success("Audio registrado")
    else:
        st.info("El audio está deshabilitado. Presiona 'Habilitar Audio' para activar.")

with col2:
    st.header("Configuración de Visualización")

    st.markdown("#### Color de Tema")
    theme_color = st.color_picker("Selecciona el color principal", "#1E90FF")

    st.markdown("#### Retroalimentación")
    st.success("Los datos se han cargado correctamente")
    st.info("Información disponible para análisis")
    st.warning("某些 registros pueden requerir validación")
    st.error("Error en la conexión de datos")

if st.session_state.data is not None:
    df = st.session_state.data

    st.markdown("---")
    st.header("Filtros y Controles")

    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("#### Seleccionar Departamento")
        departamentos = df["DPTO_CCDGO"].unique()
        selected_deptos = st.multiselect(
            "Departamentos a analizar",
            options=sorted(departamentos),
            default=None,
            help="Selecciona uno o más departamentos",
        )

    with col4:
        st.markdown("#### Control Segmentado")
        opciones_segmento = ["Todos", "Principales", "Secundarios"]
        segmento_seleccionado = st.segmented_control(
            "Ver por categoría", opciones_segmento, default="Todos"
        )

    with col5:
        st.markdown("#### Selector de Rango")
        num_min, num_max = st.select_slider(
            "Rango de códigos de municipio",
            options=sorted(df["DPTOMPIO"].unique()),
            value=(
                sorted(df["DPTOMPIO"].unique())[0],
                sorted(df["DPTOMPIO"].unique())[100],
            ),
        )

    st.markdown("---")

    col6, col7, col8 = st.columns(3)

    with col6:
        st.markdown("#### Entrada Numérica")
        limite_registros = st.number_input(
            "Número máximo de registros a mostrar",
            min_value=1,
            max_value=len(df),
            value=50,
            step=10,
        )

    with col7:
        st.markdown("#### Fecha y Hora del Análisis")
        fecha_seleccionada = st.date_input(
            "Fecha de generación del reporte", value=datetime.now().date()
        )
        hora_seleccionada = st.time_input(
            "Hora del análisis", value=datetime.now().time()
        )

    with col8:
        st.markdown("#### Checkbox de Opciones")
        mostrar_codigos = st.checkbox("Mostrar códigos de municipio", value=True)
        mostrar_nombres = st.checkbox("Mostrar nombres", value=True)
        ordenar_alfabetico = st.checkbox("Ordenar alfabéticamente", value=True)
        solo_capitales = st.checkbox("Solo capitales")

    st.markdown("---")

    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

    with col_btn1:
        btn_aplicar = st.button(
            "Aplicar Filtros", type="primary", use_container_width=True
        )

    with col_btn2:
        btn_limpiar = st.button("Limpiar Filtros", use_container_width=True)

    with col_btn3:
        btn_exportar = st.button("Exportar Datos", use_container_width=True)

    with col_btn4:
        btn_estadisticas = st.button("Ver Estadísticas", use_container_width=True)

    st.markdown("---")
    st.header("Datos Filtrados")

    df_filtrado = df.copy()

    if selected_deptos:
        df_filtrado = df_filtrado[df_filtrado["DPTO_CCDGO"].isin(selected_deptos)]

    df_filtrado = df_filtrado[
        (df_filtrado["DPTOMPIO"] >= num_min) & (df_filtrado["DPTOMPIO"] <= num_max)
    ]

    df_filtrado = df_filtrado.head(limite_registros)

    if ordenar_alfabetico:
        df_filtrado = df_filtrado.sort_values("MPIO_CNMBR")

    if solo_capitales:
        capitales = [
            "MEDELLÍN",
            "BOGOTÁ, D.C.",
            "CALI",
            "BARRANQUILLA",
            "CARTAGENA DE INDIAS",
            "SANTA MARTA",
            "IBAGUÉ",
            "MANIZALES",
            "NEIVA",
            "PEREIRA",
            "BUCARAMANGA",
            "CÚCUTA",
            "POPAYÁN",
            "FLORENCIA",
            "QUIBDÓ",
            "MONTERÍA",
            "VILLAVICENCIO",
            "PASTO",
            "ARMENIA",
            "SINCELEJO",
            "VALLEDUPAR",
            "QUIBDÓ",
            "TUNJA",
        ]
        df_filtrado = df_filtrado[df_filtrado["MPIO_CNMBR"].isin(capitales)]

    columnas_mostrar = []
    if mostrar_codigos:
        columnas_mostrar.append("DPTOMPIO")
    if mostrar_nombres:
        columnas_mostrar.append("MPIO_CNMBR")
    columnas_mostrar.extend(["DPTO_CCDGO", "MPIO_CCDGO", "MPIO_CCNCT"])

    df_display = df_filtrado[columnas_mostrar]

    st.dataframe(df_display, use_container_width=True, height=400)

    st.markdown(f"**Total de registros mostrados:** {len(df_filtrado)}")

    if btn_estadisticas:
        st.markdown("---")
        st.header("Estadísticas")

        col_est1, col_est2, col_est3 = st.columns(3)

        with col_est1:
            st.metric("Total Departamentos", len(df["DPTO_CCDGO"].unique()))

        with col_est2:
            st.metric("Total Municipios", len(df))

        with col_est3:
            st.metric("Municipios Filtrados", len(df_filtrado))

        st.markdown("#### Distribución por Departamento")
        deptos_count = df_filtrado["DPTO_CCDGO"].value_counts().head(10)
        st.bar_chart(deptos_count)

    if btn_exportar:
        csv_data = df_filtrado.to_csv(index=False)
        st.download_button(
            label="Descargar CSV filtrado",
            data=csv_data,
            file_name="municipios_filtrados.csv",
            mime="text/csv",
        )

else:
    st.info("👆 Carga el archivo CSV para comenzar el análisis")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <p>Dashboard de Análisis de Municipios de Colombia</p>
        <p>Desarrollado con Streamlit | Datos: MunicipiosVeredas.csv</p>
    </div>
    """,
    unsafe_allow_html=True,
)
