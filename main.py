import modelo
import utils
from colorama import Fore

def pedir_datos():
    print("\nCompleta los datos del nuevo jugador.")
    nombre = input("Nombre: ")
    uid = input("UID: ")
    rango = input("Rango: ")

    while True:
        try:
            kills = int(input("Kills: "))
            break
        except ValueError:
            print(Fore.RED + "Debes ingresar un número.")

    while True:
        try:
            partidas = int(input("Partidas jugadas: "))
            break
        except ValueError:
            print(Fore.RED + "Debes ingresar un número.")

    personaje = input("Personaje favorito: ")

    utils.mostrar_clanes()
    clanes_disponibles = modelo.cargar_clanes()
    while True:
        clan = input("Selecciona un clan: ").upper()
        if clan in clanes_disponibles:
            break
        else:
            print(Fore.RED + "Clan inválido. Intenta de nuevo.")

    activo = input("¿Activo? (sí/no): ").lower() in ["sí", "si", "yes", "1"]

    return {
        "nombre": nombre,
        "uid": uid,
        "rango": rango,
        "kills": kills,
        "partidas": partidas,
        "personaje": personaje,
        "clan": clan,
        "activo": activo
    }

def menu():
    while True:
        print(Fore.MAGENTA + "\n--- GESTOR FREE FIRE ---")
        print("1. Agregar jugador")
        print("2. Ver todos los jugadores")
        print("3. Buscar jugador por UID")
        print("4. Editar jugador")
        print("5. Eliminar jugador")
        print("6. Mostrar ranking por K/D")
        print("7. Filtrar por clan")
        print("8. Ver jugadores activos")
        print("9. Agregar nuevo clan (Admin)")
        print("10. Salir")

        op = input(Fore.YELLOW + "\nElige una opción: ")

        if op == "1":
            jugador = pedir_datos()
            modelo.agregar_jugador(jugador)

        elif op == "2":
            modelo.mostrar_jugadores()

        elif op == "3":
            uid = input("UID a buscar: ")
            j = modelo.buscar_jugador(uid)
            print(j if j else Fore.RED + "No encontrado.")

        elif op == "4":
            uid = input("UID del jugador: ")
            campo = input("Campo a editar (nombre, rango, kills, partidas, personaje, clan, activo): ").lower()
            valor = input("Nuevo valor: ")
            modelo.editar_jugador(uid, campo, valor)

        elif op == "5":
            uid = input("UID a eliminar: ")
            modelo.eliminar_jugador(uid)

        elif op == "6":
            utils.ranking_top_kd()

        elif op == "7":
            clan = input("Nombre del clan: ")
            utils.filtrar_por_clan(clan)

        elif op == "8":
            utils.mostrar_activos()

        elif op == "9":
            utils.agregar_clan()

        elif op == "10":
            print(Fore.GREEN + "Saliendo.")
            break
        else:
            print(Fore.RED + "Opción inválida.")

if __name__ == "__main__":
    menu()
