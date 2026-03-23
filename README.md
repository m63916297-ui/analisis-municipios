# Dashboard de Municipios de Colombia

Dashboard interactivo desarrollado con Streamlit para analizar datos del archivo `MunicipiosVeredas.csv`.

## Componentes Incluidos

- **File Uploader**: Carga del archivo CSV
- **Camera Input**: Captura de imágenes
- **Audio Input**: Grabación de audio
- **Color Picker**: Selección de color de tema
- **Multiselect**: Filtrado por departamentos
- **Segmented Control**: Control segmentado de categorías
- **Select Slider**: Selector de rango de códigos
- **Numeric Input**: Entrada numérica para límite de registros
- **Date/Time Input**: Selección de fecha y hora
- **Checkbox**: Opciones de visualización
- **Buttons**: Botones de acción (Aplicar, Limpiar, Exportar, Estadísticas)
- **Feedback**: Mensajes de éxito, info, warning y error
- **Pills**: Pills de selección en segmented control

## Ejecutar Localmente

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Desplegar en Streamlit Cloud

1. Sube los archivos `dashboard.py`, `requirements.txt` y `MunicipiosVeredas.csv` a GitHub
2. Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
3. Conecta tu repositorio de GitHub
4. Selecciona `dashboard.py` como archivo principal
5. Haz clic en "Deploy"

## Archivos Requeridos

- `dashboard.py`: Código principal del dashboard
- `requirements.txt`: Dependencias de Python
- `MunicipiosVeredas.csv`: Archivo de datos de municipios
