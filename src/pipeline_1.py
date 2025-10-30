import argparse
import apache_beam as beam
import os
import json
import csv


# ----------------------------
# VALORES CONSTANTES
# ----------------------------

# Nombres de los campos del archivo CSV
FIELDNAMES = [
    'Country', 'Capital', 'GDP','Population', 'Pop_Growth_Rate', 
    'Life_Expectancy', 'Median_Age', 'Urban_Population', 'Continent', 
    'Main_Official_Language', 'Currency'
]

# Columnas a seleccionar desde JSON's
COLUMNS_TO_KEEP = [
    'FanID','RaceID','Timestamp','DeviceType','EngagementMetric_secondswatched',
    'PredictionClicked','MerchandisingClicked','LocationData'
]

# ----------------------------
# CREACION DE FUNCIONES
# ----------------------------

# Función para seleccionar columnas de JSON
def select_columns(row):
    return {key: row[key] for key in COLUMNS_TO_KEEP if key in row}

# Función para parsear los nombres de los campos del CSV
def parse_csv_line(line):
    # DictReader necesita un iterable; usamos fieldnames para mapear a dict
    return next(csv.DictReader([line], fieldnames=FIELDNAMES))

# Función para formatear campo RaceID
def format_race_id(row):
    race_id = row['RaceID']
    race_id = race_id.replace(' ', '').replace('_','').replace(':','').lower()
    row['RaceID'] = race_id
    return row

# Use of Side Input ro enrich the main PCollection
def enrich_transaction(transaction, country_dict):
    country_info = country_dict.get(transaction['ViewerLocationCountry'], {'LocationData': 'UNKNOWN'})
    if country_info:
        enrichment_info = {
          'country':country_info['Country'],
          'capital':country_info['Capital'],
          'continent':country_info['Continent'],
          'official_language':country_info['Main_Official_Language'],
          'currency':country_info['Currency']
        }
        transaction['LocationData'] = enrichment_info
    return transaction



# Se llama al ejecutar el script
def run():

    # ----------------------------
    # Obtiene argumentos
    # ----------------------------

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir',
                        dest='input_dir',
                        default='input.txt',
                        help='Input file to process.')
    
    parser.add_argument('--input_side',
                    dest='input_side',
                    default='input.txt',
                    help='Input file to process.')

    parser.add_argument('--output_dir',
                        dest='output_dir',
                        required=True,
                        help='Output folder to write results to.')

    # Parsea argumentos
    known_args, pipeline_args = parser.parse_known_args()

    # Obtiene nombre de archivos JSON
    json_files = os.listdir(known_args.input_dir)
    
    # Construye ruta para lectura de archivos
    json_files = [
      known_args.input_dir + '/' + f for f in json_files
    ]

    # ----------------------------
    # Crear el objeto de pipeline
    # ----------------------------
    with beam.Pipeline(argv=pipeline_args) as pipeline:

      # Leer cada archivo JSON (cada línea es un JSON string)
      pcoll1 = pipeline | 'ReadJson1' >> beam.io.ReadFromText(json_files[0])
      pcoll2 = pipeline | 'ReadJson2' >> beam.io.ReadFromText(json_files[1])
      pcoll3 = pipeline | 'ReadJson3' >> beam.io.ReadFromText(json_files[2])

      # Combinar los tres PCollections en uno solo
      race_data = (
          (pcoll1, pcoll2, pcoll3)
          | 'CombineJSONs' >> beam.Flatten()
      )

      clean_race_data = (
        race_data
        | 'ParseJSON' >> beam.Map(json.loads)
        | 'FilterDevice' >> beam.Filter(lambda row: row['DeviceType'] != "Other")
        | 'FormatRaceID' >> beam.Map(format_race_id)
      )
      
      #clean_race_data | 'Mostrar en consola1' >> beam.Map(print)

      # Leer archivo de enriquecimiento
      side_data = (
        pipeline 
        | 'ReadSideFile' >> beam.io.ReadFromText(known_args.input_side, skip_header_lines=1)
        | 'ParseCSVFields' >> beam.Map(parse_csv_line)
        | 'MapCSVFields' >> beam.Map(lambda row: (row['Country'], row))
      )

      # Enriquecimiento de los datos
      enriched_data = (
          clean_race_data
          | 'EnrichData' >> beam.Map(
              enrich_transaction,
              country_dict=beam.pvalue.AsDict(side_data)
          )
      )

      # Convertir a JSON y seleccionar columnas
      final_data = (
        enriched_data
        | 'SelectColumns' >> beam.Map(select_columns)
        | 'ConvertJSONLines' >> beam.Map(lambda row: json.dumps(row, ensure_ascii=False))
      )

      # Mostrar & guardar achivo final
      final_data | 'Mostrar en consola' >> beam.Map(print)
      final_data | 'WriteToText' >> beam.io.WriteToText(known_args.output_dir)
      



if __name__ == '__main__':
    run()