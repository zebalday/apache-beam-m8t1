# Apache Beam M8 - Tarea 1

## 💭 Descripción del proyecto
Proyecto de ejemplo/desarrollo para el **Módulo 8 (Apache Beam / Data Pipeline)** del diplomado de **Ingeniería de Datos**.  
El objetivo principal del repo es mostrar cómo:

1. Leer **múltiples archivos JSON** que representan eventos/transacciones.
2. Leer un **archivo CSV de enriquecimiento** (`input_side/`) con información de países.
3. Convertir ese CSV en un **side input** para Apache Beam.
4. **Enriquecer** cada registro JSON con los datos del país (capital, continente, idioma, moneda, etc.).
5. Aplicar **transformaciones** sobre el flujo principal (filtros, formateo de IDs, selección de columnas).
6. Escribir el resultado final en una carpeta de salida.

> En simple: hay un **PCollection principal** (los JSON) y un **PCollection auxiliar** (CSV con países). El pipeline une ambos usando side inputs.



## 📁 Estructura del repositorio

```text
apache-beam-m8t1/
├── input/               # JSONs de entrada (stream principal)
│   ├── ...              # ej: events_1.json, events_2.json, ...
├── input_side/          # CSV de enriquecimiento (countries, capitales, idioma, moneda, etc.)
│   └── ...              # ej: countries.csv
├── src/
│   └── pipeline_1.py    # script principal de Apache Beam (entrypoint del ejercicio)
├── requirements.txt     # dependencias mínimas para correr el pipeline
└── README.md            # este archivo
```

---

## >_ Ejecución del Pipeline

Para poder ejecutar el pipeline se deben ejecutar los siguientes comandos:


**Instalar requerimientos**:
```
# Moverse a directorio
cd tarea_1/apache-beam-m8t1

# Instalar dependencias
!pip install -r requirements.txt
```

Ejecutar pipeline con los parámetros:
* **--input_dir**: Directorio para buscar los JSON.
* **--input_side**: Directorio para buscar CSV de enriquecimiento.
* **--output_dir**: Directorio y nombre de archivo final.
```
# Ejecución de pipeline con parámetros

!python src/pipeline_1.py --input_dir input --input_side input_side/country_data_v2.csv --output_dir output/results
```