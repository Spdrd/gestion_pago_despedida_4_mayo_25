import json

RUTA_DATOS = "datos.json"

def cargar_datos(ruta=RUTA_DATOS):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_datos(personas, ruta=RUTA_DATOS):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(personas, archivo, indent=4, ensure_ascii=False)

def crear_persona(nombre, ruta=RUTA_DATOS):
    personas = cargar_datos(ruta)
    if any(p["nombre"] == nombre for p in personas):
        return False  # Ya existe
    personas.append({"nombre": nombre, "pagos": []})
    guardar_datos(personas, ruta)
    return True

def agregar_pago(nombre, monto, ruta=RUTA_DATOS):
    personas = cargar_datos(ruta)
    for persona in personas:
        if persona["nombre"] == nombre:
            persona["pagos"].append(monto)
            guardar_datos(personas, ruta)
            return True
    return False  # No se encontró la persona
