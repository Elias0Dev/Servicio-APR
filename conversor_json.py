#Contexto: se exportan los datos de mysql a un json pero no es legible por el proyecto
#Solucion: este archivo convierte el json a uno legible y permite cargar los datos a las tablas correspondientes
#python manage.py dumpdata inicio.Cargo inicio.Tarifa --indent 4 > datos.json #exportar
#python manage.py loaddata datos_limpios.json #importar
#python manage.py dumpdata admin_interface.Theme --indent 4 > theme.json 


import json
import chardet  # Necesario: pip install chardet

archivo_entrada = "datos.json"
archivo_salida = "datos_limpios.json"

# Leemos el archivo en modo binario
with open(archivo_entrada, "rb") as f:
    contenido_bin = f.read()

# Detectamos codificación automáticamente
resultado = chardet.detect(contenido_bin)
encoding = resultado['encoding']
confidence = resultado['confidence']
print(f"Codificación detectada: {encoding} (confianza {confidence})")

# Decodificamos usando la codificación detectada
contenido = contenido_bin.decode(encoding)

# Cargamos JSON
datos = json.loads(contenido)

# Guardamos en UTF-8 limpio listo para Django
with open(archivo_salida, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=4)

print(f"Archivo limpio generado: {archivo_salida}")
