from colorama import init, Fore, Style
import os
import json
from pathlib import Path

init(autoreset=True)

PASSWORD = "admincaleb1234"

def get_data_folder():
    appdata = os.getenv('APPDATA')
    data_folder = os.path.join(appdata, 'GestorFreeFire')
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    return data_folder

def obtener_ruta_archivo(nombre_archivo):
    return os.path.join(get_data_folder(), nombre_archivo)

def cargar_json(nombre_archivo):
    ruta = obtener_ruta_archivo(nombre_archivo)
    if not os.path.exists(ruta):
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write('[]')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(nombre_archivo, datos):
    ruta = obtener_ruta_archivo(nombre_archivo)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Ahora las funciones originales usando la nueva forma para cargar y guardar datos

def mostrar_clanes():
    clanes = cargar_json('clanes.json')
    print("\nClanes disponibles:")
    for clan in clanes:
        print(f"- {clan}")

def agregar_clan():
    clave = input("\nIngresa la clave de administrador: ")
    if clave != PASSWORD:
        print(Fore.RED + "Clave incorrecta. No tienes permisos.")
        return
    nuevo_clan = input("Nombre del nuevo clan: ")
    clanes = cargar_json('clanes.json')
    if nuevo_clan in clanes:
        print(Fore.YELLOW + "Ese clan ya existe.")
        return
    clanes.append(nuevo_clan)
    guardar_json('clanes.json', clanes)
    print(Fore.GREEN + "Clan agregado con éxito.")

def ranking_top_kd(n=5):
    jugadores = cargar_json('jugadores.json')
    jugadores = [j for j in jugadores if j.get("partidas",0) > 0]
    jugadores.sort(key=lambda x: x["kills"] / x["partidas"], reverse=True)

    print(Fore.YELLOW + f"\n🏆 TOP {n} JUGADORES POR K/D")
    for i, j in enumerate(jugadores[:n], start=1):
        kd = j["kills"] / j["partidas"]
        print(Fore.CYAN + f"{i}. {j['nombre']} (K/D: {kd:.2f})")

def filtrar_por_clan(clan):
    clan = clan.upper()
    clanes = cargar_json('clanes.json')
    if clan not in [c.upper() for c in clanes]:
        print(Fore.RED + "Clan inválido. Usa uno de la lista disponible.")
        mostrar_clanes()
        return

    jugadores = cargar_json('jugadores.json')
    filtrados = [j for j in jugadores if j.get("clan","").upper() == clan]

    if not filtrados:
        print(Fore.RED + "No se encontraron jugadores en ese clan.")
    else:
        print(Fore.GREEN + f"\nMiembros del clan '{clan}':")
        for j in filtrados:
            print(Fore.CYAN + f"- {j['nombre']} ({j['rango']})")

def mostrar_activos():
    jugadores = cargar_json('jugadores.json')
    activos = [j for j in jugadores if j.get("activo", False)]

    if not activos:
        print(Fore.RED + "No hay jugadores activos.")
    else:
        print(Fore.GREEN + "\nJugadores activos:")
        for j in activos:
            print(Fore.CYAN + f"- {j['nombre']} ({j['rango']})")
