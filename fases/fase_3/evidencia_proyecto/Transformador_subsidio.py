import json
from datetime import datetime

def convertir_fecha(fecha_raw):
    """
    Convierte 'DD-MM-YYYY 0:00' a 'YYYY-MM-DD'
    y repara fechas inválidas como '00-01-1900'
    """
    fecha_raw = fecha_raw.split(" ")[0]  # eliminar hora

    dia, mes, anio = fecha_raw.split("-")

    # Reparar día "00"
    if dia == "00":
        dia = "01"

    fecha_limpia = f"{dia}-{mes}-{anio}"

    try:
        fecha_dt = datetime.strptime(fecha_limpia, "%d-%m-%Y")
        return fecha_dt.strftime("%Y-%m-%d")
    except ValueError:
        # Última defensa: fecha inválida → None
        return None


def transformar_json(entrada, nombre_modelo="inicio.subsidio"):
    salida = []

    for idx, item in enumerate(entrada, start=1):

        fecha_formateada = convertir_fecha(item["fecha_aplicacion"])

        fixture_item = {
            "model": nombre_modelo,
            "pk": idx,
            "fields": {
                "cliente": int(item["id_cliente"]),
                "num_decreto": item["﻿num_decreto"].replace("\ufeff", ""),
                "tramo_rsh": item["tramo_rsh"],
                "monto": item["monto"],
                "fecha_aplicacion": fecha_formateada,
            }
        }

        salida.append(fixture_item)

    return salida


# ---------- USO ----------
with open("subsidio.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

resultado = transformar_json(datos)

with open("subsidio_django.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

print("¡Transformación completa!")
