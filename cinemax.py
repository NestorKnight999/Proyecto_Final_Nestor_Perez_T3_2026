from cartelera import cartelera

FILAS = 5
COLUMNAS = 6
LETRAS = "ABCDE"

asientos = {}
nombres = {}

for dia in cartelera:
    for funcion in cartelera[dia]:
        clave = dia + "-" + str(funcion["sala"]) + "-" + funcion["horario"]
        matriz = []
        for i in range(FILAS):
            fila = []
            for j in range(COLUMNAS):
                fila.append(".")
            matriz.append(fila)
        asientos[clave] = matriz


def hacer_clave(dia, funcion):
    return dia + "-" + str(funcion["sala"]) + "-" + funcion["horario"]


def pedir_dia():
    dia = input("Dia de la semana: ").strip().capitalize()
    if dia == "Miercoles":
        dia = "Miércoles"
    if dia == "Sabado":
        dia = "Sábado"
    if dia not in cartelera:
        print("Ese dia no existe.")
        return None
    return dia


def pedir_funcion(dia):
    sala = input("Sala (1-5): ").strip()
    horario = input("Horario (ej: 2:00 pm): ").strip().lower()
    if not sala.isdigit():
        print("La sala debe ser un numero.")
        return None
    for funcion in cartelera[dia]:
        if funcion["sala"] == int(sala) and funcion["horario"] == horario:
            return funcion
    print("Ese dia no hay funcion en esa sala a ese horario.")
    return None


def pedir_asiento():
    asiento = input("Asiento (ej: C3): ").strip().upper()
    if len(asiento) < 2:
        print("Asiento invalido.")
        return None
    letra = asiento[0]
    numero = asiento[1:]
    if letra not in LETRAS or not numero.isdigit():
        print("Asiento invalido.")
        return None
    columna = int(numero) - 1
    if columna < 0 or columna >= COLUMNAS:
        print("Ese asiento no existe en la sala.")
        return None
    fila = LETRAS.index(letra)
    return asiento, fila, columna


def ver_cartelera():
    dia = pedir_dia()
    if dia is None:
        return
    print("\nCartelera del", dia)
    print("-" * 50)
    for f in cartelera[dia]:
        print("Sala", f["sala"], "|", f["horario"], "|", f["formato"], "|", f["pelicula"])


def mostrar_matriz(dia, funcion):
    clave = hacer_clave(dia, funcion)
    matriz = asientos[clave]
    print("\n" + funcion["pelicula"], "-", funcion["formato"])
    print("Sala", funcion["sala"], "|", dia, "|", funcion["horario"])
    print("\n    1 2 3 4 5 6")
    for i in range(FILAS):
        linea = LETRAS[i] + "   "
        for j in range(COLUMNAS):
            linea = linea + matriz[i][j] + " "
        print(linea)
    print("\n. = libre   X = ocupado")


def mostrar_asientos():
    dia = pedir_dia()
    if dia is None:
        return
    funcion = pedir_funcion(dia)
    if funcion is None:
        return
    mostrar_matriz(dia, funcion)


def reservar():
    dia = pedir_dia()
    if dia is None:
        return
    funcion = pedir_funcion(dia)
    if funcion is None:
        return
    mostrar_matriz(dia, funcion)
    datos = pedir_asiento()
    if datos is None:
        return
    asiento, fila, columna = datos
    clave = hacer_clave(dia, funcion)
    if asientos[clave][fila][columna] == "X":
        print("Ese asiento ya esta ocupado.")
        return
    nombre = input("Nombre de quien reserva: ").strip()
    asientos[clave][fila][columna] = "X"
    nombres[clave + "-" + asiento] = nombre
    print("\nReserva confirmada!")
    print("Nombre:", nombre)
    print("Pelicula:", funcion["pelicula"], "(" + funcion["formato"] + ")")
    print("Dia:", dia, "| Sala", funcion["sala"], "|", funcion["horario"])
    print("Asiento:", asiento)


def cancelar():
    dia = pedir_dia()
    if dia is None:
        return
    funcion = pedir_funcion(dia)
    if funcion is None:
        return
    datos = pedir_asiento()
    if datos is None:
        return
    asiento, fila, columna = datos
    clave = hacer_clave(dia, funcion)
    if asientos[clave][fila][columna] == ".":
        print("Ese asiento no esta reservado.")
        return
    asientos[clave][fila][columna] = "."
    llave = clave + "-" + asiento
    if llave in nombres:
        del nombres[llave]
    print("Reserva del asiento", asiento, "cancelada.")


def ver_disponibilidad():
    dia = pedir_dia()
    if dia is None:
        return
    print("\nDisponibilidad del", dia)
    print("-" * 60)
    total = FILAS * COLUMNAS
    for f in cartelera[dia]:
        matriz = asientos[hacer_clave(dia, f)]
        ocupados = 0
        for fila in matriz:
            for a in fila:
                if a == "X":
                    ocupados = ocupados + 1
        libres = total - ocupados
        porcentaje = ocupados / total * 100
        print("Sala", f["sala"], "|", f["horario"], "|", f["pelicula"])
        print("   Libres:", libres, "| Ocupados:", ocupados, "| Ocupacion:", round(porcentaje), "%")


def menu():
    while True:
        print("\n===== CineMax - Sistema de Reservas =====")
        print("1. Ver cartelera de un día")
        print("2. Mostrar asientos de una función")
        print("3. Reservar asiento")
        print("4. Cancelar reserva")
        print("5. Ver disponibilidad")
        print("6. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ver_cartelera()
        elif opcion == "2":
            mostrar_asientos()
        elif opcion == "3":
            reservar()
        elif opcion == "4":
            cancelar()
        elif opcion == "5":
            ver_disponibilidad()
        elif opcion == "6":
            print("Gracias por usar CineMax!")
            break
        else:
            print("Opcion invalida, intente de nuevo.")


menu()
