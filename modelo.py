import os
import json
from pathlib import Path

def get_data_folder():
    appdata = os.getenv('APPDATA')
    data_folder = os.path.join(appdata, 'GestorFreeFire')
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    return data_folder

def obtener_ruta_archivo(nombre_archivo):
    return os.path.join(get_data_folder(), nombre_archivo)

# Manejo de clanes

def cargar_clanes():
    archivo = obtener_ruta_archivo('clanes.json')
    if not os.path.exists(archivo):
        clanes = [
            "FIREGODS",
            "SHADOWCREW",
            "ALPHASQUAD",
            "LOS CAGAFUEGO",
            "DEMON KINGS"
        ]
        guardar_clanes(clanes)
        return clanes
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_clanes(clanes):
    archivo = obtener_ruta_archivo('clanes.json')
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(clanes, f, indent=4, ensure_ascii=False)

def agregar_clan(nuevo_clan):
    clanes = cargar_clanes()
    nuevo_clan = nuevo_clan.upper()
    if nuevo_clan in clanes:
        print("Ese clan ya existe.")
        return
    clanes.append(nuevo_clan)
    guardar_clanes(clanes)
    print(f"Clan '{nuevo_clan}' añadido.")

# CRUD de jugadores

def cargar_datos():
    archivo = obtener_ruta_archivo('datos.json')
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_datos(jugadores):
    archivo = obtener_ruta_archivo('datos.json')
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(jugadores, f, indent=4, ensure_ascii=False)

def agregar_jugador(jugador):
    jugadores = cargar_datos()
    if any(j["uid"] == jugador["uid"] for j in jugadores):
        print("Ya existe un jugador con ese UID.")
        return
    jugadores.append(jugador)
    guardar_datos(jugadores)
    print("Jugador agregado.")

def mostrar_jugadores():
    jugadores = cargar_datos()
    for j in jugadores:
        print(j)

def buscar_jugador(uid):
    jugadores = cargar_datos()
    for j in jugadores:
        if j["uid"] == uid:
            return j
    return None

def editar_jugador(uid, campo, nuevo_valor):
    jugadores = cargar_datos()
    for j in jugadores:
        if j["uid"] == uid:
            if campo in j:
                if campo in ["kills", "partidas"]:
                    try:
                        nuevo_valor = int(nuevo_valor)
                    except ValueError:
                        print("Valor inválido para kills o partidas.")
                        return
                elif campo == "activo":
                    nuevo_valor = str(nuevo_valor).lower() in ["true", "1", "sí", "si"]
                j[campo] = nuevo_valor
                guardar_datos(jugadores)
                print("Jugador actualizado.")
                return
            else:
                print("Campo inválido.")
                return
    print("Jugador no encontrado.")

def eliminar_jugador(uid):
    jugadores = cargar_datos()
    nuevos = [j for j in jugadores if j["uid"] != uid]
    if len(jugadores) == len(nuevos):
        print("Jugador no encontrado.")
        return
    guardar_datos(nuevos)
    print("Jugador eliminado.")
