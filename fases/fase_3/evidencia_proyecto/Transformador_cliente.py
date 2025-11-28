import json

# Leer el JSON original
with open("Cliente.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

json_salida = []

for cliente in datos:
    # Obtener PK, limpiando posibles caracteres invisibles
    pk_str = cliente.get("id_cliente") or cliente.get("﻿id_cliente")
    pk = int(pk_str) if pk_str and pk_str.isdigit() else 0

    # Obtener RUT de forma segura
    rut_str = cliente.get("rut", "")
    try:
        rut = int(rut_str) if rut_str.strip() != "" else 0
    except ValueError:
        rut = 0  # si hay caracteres no numéricos, asignamos 0

    entry = {
        "model": "inicio.cliente",
        "pk": pk,
        "fields": {
            "nombre": cliente.get("nombre", ""),
            "rut": rut,
            "dv": cliente.get("dv", ""),
            "tipo": "persona",
            "razon_social": cliente.get("razon_social", "No Aplica"),
            "sector": cliente.get("sector", "No Aplica"),
            "direccion": cliente.get("direccion", "No Aplica"),
            "telefono": int(cliente.get("telefono", 0)) if cliente.get("telefono") else 0,
            "email": cliente.get("email", "No Aplica"),
            "numero_medidor": cliente.get("numero_medidor", "")
        }
    }
    json_salida.append(entry)

# Guardar JSON listo para Django
with open("clientes_django.json", "w", encoding="utf-8") as f:
    json.dump(json_salida, f, ensure_ascii=False, indent=4)

print("JSON listo para loaddata generado: clientes_django.json")
