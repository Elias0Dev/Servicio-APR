import json
from datetime import datetime

# -------- Helpers --------

def parse_bool(value):
    # Entrada "0" o "1", salida True/False
    return value == "1"

def parse_date(value):
    # Entrada: "04-11-2025 0:00"
    # Salida:  "2025-11-04"
    try:
        fecha = value.split(" ")[0]  # quitar hora
        return datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
    except:
        return None

# -------- Transformador principal --------

def transformar_json_a_fixture(input_file, output_file="facturas_django.json"):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    salida = []

    for i, row in enumerate(data, start=1):
        factura = {
            "model": "inicio.factura",
            "pk": i,
            "fields": {
                "id_cliente": int(row["id_cliente"]),
                "total_pagar": f'{float(row["﻿total_pagar"]):.2f}',
                "fecha_emision": parse_date(row["fecha_emision"]),
                "fecha_vencimiento": parse_date(row["fecha_vencimiento"]),
                "estado_pago": parse_bool(row["estado_pago"]),
                "corte": parse_bool(row["corte"]),
                "subsidio": parse_bool(row["subsidio"]),
                "lectura_anterior": int(row["lectura_anterior"]),
                "lectura_actual": int(row["lectura_actual"]),
                "fecha_actual": parse_date(row["fecha_actual"]),
                "fecha_anterior": parse_date(row["fecha_anterior"]),
                "consumo": int(row["consumo"])
            }
        }

        salida.append(factura)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(salida, f, indent=4, ensure_ascii=False)

    print(f"✔ Archivo generado: {output_file}")

# -------- Ejecutar --------

if __name__ == "__main__":
    transformar_json_a_fixture("Factura.json")
