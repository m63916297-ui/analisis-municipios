import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="Dashboard Municipios Colombia", layout="wide")

st.title("Dashboard de Análisis - Municipios de Colombia")
st.markdown("---")

if "data" not in st.session_state:
    st.session_state.data = None

col1, col2 = st.columns([1, 1])

with col1:
    st.header(":file_folder: Carga de Datos")

    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, encoding="utf-8")
        st.session_state.data = df
        st.success(f"✅ Archivo cargado: {uploaded_file.name}")
        st.info(f"📊 Total de registros: {len(df)}")
    else:
        st.warning("⚠️ Por favor carga el archivo MunicipiosVeredas.csv")

    st.markdown("### 🎤 Entrada de Audio")

    col_aud_btn, col_aud_status = st.columns([1, 2])

    with col_aud_btn:
        if st.button(
            "🎤 Habilitar Audio", key="btn_audio_toggle", use_container_width=True
        ):
            if "audio_enabled" not in st.session_state:
                st.session_state.audio_enabled = False
            st.session_state.audio_enabled = not st.session_state.audio_enabled

    with col_aud_status:
        if st.session_state.get("audio_enabled", False):
            st.success("Audio: HABILITADO")
        else:
            st.warning("Audio: DESHABILITADO")

    if st.session_state.get("audio_enabled", False):
        audio_input = st.audio_input("Graba un audio con observaciones")
        if audio_input:
            st.audio(audio_input)
            st.success("Audio registrado")
    else:
        st.info("El audio está deshabilitado. Presiona 'Habilitar Audio' para activar.")

with col2:
    st.header(":art: Configuración de Visualización")

    st.markdown("#### 🎨 Color de Tema")
    theme_color = st.color_picker("Selecciona el color principal", "#1E90FF")

    st.markdown("#### 💬 Retroalimentación")
    st.success("✅ Los datos se han cargado correctamente")
    st.info("ℹ️ Información disponible para análisis")
    st.warning("⚠️ Ciertos registros pueden requerir validación")
    st.error("❌ Error en la conexión de datos")

if st.session_state.data is not None:
    df = st.session_state.data

    st.markdown("---")
    st.header(":filter: Filtros y Controles")

    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("#### 🏛️ Seleccionar Departamento")
        departamentos = df["DPTO_CCDGO"].unique()
        selected_deptos = st.multiselect(
            "Departamentos a analizar",
            options=sorted(departamentos),
            default=None,
            help="Selecciona uno o más departamentos",
        )

    with col4:
        st.markdown("#### 📋 Control Segmentado")
        opciones_segmento = ["Todos", "Principales", "Secundarios"]
        segmento_seleccionado = st.segmented_control(
            "Ver por categoría", opciones_segmento, default="Todos"
        )

    with col5:
        st.markdown("#### 🎚️ Selector de Rango")
        num_min, num_max = st.select_slider(
            "Rango de códigos de municipio",
            options=sorted(df["DPTOMPIO"].unique()),
            value=(
                sorted(df["DPTOMPIO"].unique())[0],
                sorted(df["DPTOMPIO"].unique())[100],
            ),
        )

    st.markdown("---")

    col6, col7 = st.columns(2)

    with col6:
        st.markdown("#### 🔢 Entrada Numérica")
        limite_registros = st.number_input(
            "Número máximo de registros a mostrar",
            min_value=1,
            max_value=len(df),
            value=50,
            step=10,
        )

    with col7:
        st.markdown("#### ☑️ Checkbox de Opciones")
        mostrar_codigos = st.checkbox("Mostrar códigos de municipio", value=True)
        mostrar_nombres = st.checkbox("Mostrar nombres", value=True)
        ordenar_alfabetico = st.checkbox("Ordenar alfabéticamente", value=True)
        solo_capitales = st.checkbox("Solo capitales")
        mostrar_graficos = st.checkbox("Mostrar gráficos adicionales", value=True)

    st.markdown("---")

    st.header(":control_buttons: Acciones")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

    with col_btn1:
        btn_aplicar = st.button(
            "🔍 Aplicar Filtros", type="primary", use_container_width=True
        )

    with col_btn2:
        btn_limpiar = st.button("🗑️ Limpiar Filtros", use_container_width=True)

    with col_btn3:
        btn_exportar = st.button("📥 Exportar Datos", use_container_width=True)

    with col_btn4:
        btn_estadisticas = st.button("📈 Ver Estadísticas", use_container_width=True)

    st.markdown("---")
    st.header(":bar_chart: Resultados del Análisis")

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
            "TUNJA",
            "CARTAGENA",
        ]
        df_filtrado = df_filtrado[df_filtrado["MPIO_CNMBR"].isin(capitales)]

    if btn_limpiar:
        st.session_state.data = None
        st.rerun()

    st.subheader(f"📊 Resumen: {len(df_filtrado)} municipios encontrados")

    col_metrics1, col_metrics2, col_metrics3, col_metrics4 = st.columns(4)

    with col_metrics1:
        st.metric("📍 Total Filtrado", len(df_filtrado))

    with col_metrics2:
        st.metric("🏛️ Departamentos", df_filtrado["DPTO_CCDGO"].nunique())

    with col_metrics3:
        st.metric("📋 Códigos Únicos", df_filtrado["DPTOMPIO"].nunique())

    with col_metrics4:
        st.metric("📄 Registros Originales", len(df))

    st.markdown("---")

    st.subheader("📋 Tabla Completa de Resultados")

    columnas_mostrar = []
    if mostrar_codigos:
        columnas_mostrar.append("DPTOMPIO")
    if mostrar_nombres:
        columnas_mostrar.append("MPIO_CNMBR")
    columnas_mostrar.extend(["DPTO_CCDGO", "MPIO_CCDGO", "MPIO_CCNCT"])

    df_display = df_filtrado[columnas_mostrar].reset_index(drop=True)
    df_display.index = df_display.index + 1
    df_display.index.name = "N°"

    st.dataframe(df_display, use_container_width=True, height=400)

    st.markdown("---")

    if mostrar_graficos:
        st.subheader("📊 Visualizaciones Detalladas")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("##### Distribución por Departamento")
            deptos_count = df_filtrado["DPTO_CCDGO"].value_counts().reset_index()
            deptos_count.columns = ["Departamento", "Cantidad"]

            fig_bar = px.bar(
                deptos_count,
                x="Departamento",
                y="Cantidad",
                color="Cantidad",
                color_continuous_scale="Viridis",
                title="Municipios por Departamento",
            )
            fig_bar.update_layout(
                xaxis_title="Código Departamento",
                yaxis_title="Cantidad de Municipios",
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_chart2:
            st.markdown("##### Distribución Porcentual")
            deptos_pie = df_filtrado["DPTO_CCDGO"].value_counts().reset_index()
            deptos_pie.columns = ["Departamento", "Cantidad"]

            fig_pie = px.pie(
                deptos_pie,
                values="Cantidad",
                names="Departamento",
                title="Porcentaje por Departamento",
                hole=0.4,
            )
            fig_pie.update_layout(showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)

        col_chart3, col_chart4 = st.columns(2)

        with col_chart3:
            st.markdown("##### Municipios por Código (Top 20)")
            top_municipios = df_filtrado.nlargest(20, "DPTOMPIO")

            fig_scatter = px.scatter(
                top_municipios,
                x="DPTOMPIO",
                y="DPTO_CCDGO",
                size=[10] * len(top_municipios),
                color="MPIO_CNMBR",
                hover_name="MPIO_CNMBR",
                title="Top 20 Municipios por Código",
            )
            fig_scatter.update_layout(
                xaxis_title="Código Municipio",
                yaxis_title="Código Departamento",
                showlegend=True,
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col_chart4:
            st.markdown("##### Histograma de Códigos")
            fig_hist = px.histogram(
                df_filtrado,
                x="DPTOMPIO",
                nbins=20,
                title="Distribución de Códigos de Municipio",
                color_discrete_sequence=["#1E90FF"],
            )
            fig_hist.update_layout(
                xaxis_title="Código Municipio",
                yaxis_title="Frecuencia",
                showlegend=False,
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("---")
        st.subheader("📈 Análisis Estadístico")

        col_stats1, col_stats2 = st.columns(2)

        with col_stats1:
            st.markdown("##### Estadísticas Descriptivas")
            stats_df = df_filtrado[["DPTOMPIO", "DPTO_CCDGO", "MPIO_CCDGO"]].describe()
            st.dataframe(stats_df, use_container_width=True)

        with col_stats2:
            st.markdown("##### Primeros 10 Municipios")
            top10 = df_filtrado.head(10)[["MPIO_CNMBR", "DPTO_CCDGO", "DPTOMPIO"]]
            st.dataframe(top10, use_container_width=True)

    if btn_estadisticas:
        st.markdown("---")
        st.header("📊 Panel de Estadísticas Completas")

        col_est1, col_est2, col_est3 = st.columns(3)

        with col_est1:
            st.metric("Total Departamentos", len(df["DPTO_CCDGO"].unique()))

        with col_est2:
            st.metric("Total Municipios", len(df))

        with col_est3:
            st.metric("Municipios Filtrados", len(df_filtrado))

        st.markdown("##### Evolución por Departamento")
        deptos_evol = (
            df_filtrado.groupby("DPTO_CCDGO").size().reset_index(name="Cantidad")
        )
        deptos_evol = deptos_evol.sort_values("Cantidad", ascending=False)

        fig_line = px.line(
            deptos_evol,
            x="DPTO_CCDGO",
            y="Cantidad",
            markers=True,
            title="Cantidad de Municipios por Departamento",
        )
        fig_line.update_layout(xaxis_title="Departamento", yaxis_title="Cantidad")
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("##### Tabla Detallada de Departamentos")
        tabla_deptos = (
            df_filtrado.groupby("DPTO_CCDGO")
            .agg({"MPIO_CNMBR": "count", "DPTOMPIO": ["min", "max"]})
            .reset_index()
        )
        tabla_deptos.columns = ["Depto", "Total_Municipios", "Cod_Min", "Cod_Max"]
        st.dataframe(tabla_deptos, use_container_width=True)

    if btn_exportar:
        csv_data = df_filtrado.to_csv(index=False)
        st.download_button(
            label="⬇️ Descargar CSV filtrado",
            data=csv_data,
            file_name="municipios_filtrados.csv",
            mime="text/csv",
        )

        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            df_filtrado.to_excel(writer, sheet_name="Municipios", index=False)
        st.download_button(
            label="📊 Descargar Excel",
            data=excel_buffer.getvalue(),
            file_name="municipios_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

else:
    st.info("👆 Carga el archivo CSV para comenzar el análisis")

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <p><strong>Dashboard de Análisis de Municipios de Colombia</strong></p>
        <p>Desarrollado con Streamlit | Datos: MunicipiosVeredas.csv</p>
        <p>Componentes: File Uploader, Audio Input, Color Picker, Multiselect, Segmented Control, 
        Select Slider, Number Input, Checkbox, Buttons, Feedback</p>
    </div>
    """,
    unsafe_allow_html=True,
)

import io
