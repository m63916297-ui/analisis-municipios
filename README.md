# Dashboard de Municipios de Colombia

Dashboard interactivo desarrollado con **Streamlit** y **Plotly** para analizar datos del archivo `MunicipiosVeredas.csv`.

## Componentes Incluidos

### Elementos de Entrada
- **File Uploader** 📁 - Carga del archivo CSV
- **Audio Input** 🎤 - Grabación de audio con habilitación/deshabilitación
- **Text Area** 📝 - Transcripción y traducción de audio
- **Color Picker** 🎨 - Selección de color de tema

### Controles de Filtro
- **Multiselect** 🏛️ - Filtrado por departamentos
- **Segmented Control** 📋 - Control segmentado de categorías
- **Select Slider** 🎚️ - Selector de rango de códigos de municipio
- **Numeric Input** 🔢 - Límite de registros a mostrar

### Opciones de Visualización
- **Checkbox** ☑️ - Opciones de visualización (códigos, nombres, orden, capitales)
- **Buttons** 🔘 - Acciones (Aplicar, Limpiar, Exportar, Estadísticas)
- **Feedback** 💬 - Mensajes de éxito, info, warning y error

### Visualización de Datos
- **Pandas DataFrame** 📊 - Tabla completa de resultados
- **Plotly Charts** 📈 - Gráficos interactivos:
  - Gráfico de barras
  - Gráfico de pastel
  - Scatter plot
  - Histograma
  - Gráfico de líneas

### Exportación
- **CSV** - Exportar datos filtrados
- **Excel** - Exportar a formato .xlsx
- **JSON** - Exportar transcripciones y metadata

## Requisitos

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.18.0
openpyxl>=3.1.0
```

## Ejecutar Localmente

```bash
cd analisis
pip install -r requirements.txt
streamlit run dashboard.py
```

## Desplegar en Streamlit Cloud

1. Sube los archivos a tu repositorio de GitHub:
   - `dashboard.py`
   - `requirements.txt`
   - `MunicipiosVeredas.csv`

2. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)

3. Conecta tu repositorio de GitHub

4. Selecciona `dashboard.py` como archivo principal

5. Haz clic en **"Deploy"**

## Archivos del Proyecto

```
analisis/
├── dashboard.py          # Código principal del dashboard
├── requirements.txt     # Dependencias de Python
├── README.md            # Este archivo
└── MunicipiosVeredas.csv # Archivo de datos de municipios
```

## Funcionalidades Principales

### 1. Carga de Datos
- Carga archivos CSV de municipios
- Validación automática del formato
- Contador de registros

### 2. Entrada de Audio
- Habilitar/deshabilitar micrófono
- Grabación de audio
- Transcripción manual
- Traducción entre idiomas
- Exportación a JSON

### 3. Filtros y Análisis
- Filtrado por departamento
- Rango de códigos de municipio
- Límite de registros
- Ordenamiento alfabético
- Solo capitales

### 4. Visualizaciones
- Tabla completa con numeración
- Gráficos interactivos de distribución
- Estadísticas descriptivas
- Panel de estadísticas avanzadas

### 5. Exportación
- CSV filtrado
- Excel con formato
- JSON con metadata

## Estructura del JSON Exportado

```json
{
  "metadata": {
    "fecha_creacion": "2024-01-01 12:00:00",
    "idioma_origen": "Español",
    "idioma_traduccion": "Inglés",
    "usuario": "Dashboard Municipios Colombia"
  },
  "audio": {
    "habilitado": true,
    "transcripcion": "Texto transcrito..."
  },
  "datos_csv": {
    "total_registros": 1122,
    "fecha_analisis": "2024-01-01"
  },
  "transcripcion": {
    "texto_original": "...",
    "traduccion": "Español → Inglés",
    "fecha_transcripcion": "2024-01-01 12:00:00"
  }
}
```

## Tecnologías

- **Streamlit** - Framework web
- **Pandas** - Manipulación de datos
- **Plotly** - Visualizaciones interactivas
- **Python** - Lenguaje de programación

---

**Desarrollado con Streamlit** | Datos: MunicipiosVeredas.csv
