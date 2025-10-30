# Apache Beam M8 - Tarea 1

Proyecto de ejemplo/desarrollo para el **Módulo 8 (Apache Beam / Data Pipeline)** del diplomado de **Ingeniería de Datos**.  
El objetivo principal del repo es mostrar cómo:

1. Leer **múltiples archivos JSON** que representan eventos/transacciones.
2. Leer un **archivo CSV de enriquecimiento** (`input_side/`) con información de países.
3. Convertir ese CSV en un **side input** para Apache Beam.
4. **Enriquecer** cada registro JSON con los datos del país (capital, continente, idioma, moneda, etc.).
5. Aplicar **transformaciones** sobre el flujo principal (filtros, formateo de IDs, selección de columnas).
6. Escribir el resultado final en una carpeta de salida.

> En simple: hay un **PCollection principal** (los JSON) y un **PCollection auxiliar** (CSV con países). El pipeline une ambos usando side inputs.

---

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
