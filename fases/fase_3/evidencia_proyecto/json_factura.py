import csv
import json

# Nombre del archivo CSV
csv_file = 'Factura.csv'
# Nombre del archivo JSON de salida
json_file = 'Factura.json'

# Abrimos el CSV y leemos los datos
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')  # Especificamos que el separador es ;
    rows = list(reader)

# Guardamos los datos en formato JSON
with open(json_file, mode='w', encoding='utf-8') as f:
    json.dump(rows, f, indent=4, ensure_ascii=False)

print(f"Archivo {json_file} generado correctamente.")
