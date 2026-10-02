from cartelera import cartelera
 
FILAS = 5
COLUMNAS = 6
LETRAS = "ABCDE"
 
asientos = {}
nombres = {}
 
 
def hacer_clave(dia, funcion):
    return dia + "-" + str(funcion["sala"]) + "-" + funcion["horario"]
 
 
for dia in cartelera:
    for funcion in cartelera[dia]:
        matriz = []
        for i in range(FILAS):
            fila = []
            for j in range(COLUMNAS):
                fila.append(".")
            matriz.append(fila)
        asientos[hacer_clave(dia, funcion)] = matriz
 
 
def sin_acentos(texto):
    texto = texto.lower()
    for a, b in [("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u")]:
        texto = texto.replace(a, b)
    return texto
 
 
def contar_ocupados(clave):
    ocupados = 0
    for fila in asientos[clave]:
        for a in fila:
            if a == "X":
                ocupados = ocupados + 1
    return ocupados
 
 
def pedir_dia():
    while True:
        entrada = input("\nDecida el día: Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo\n(Escriba 0 para volver al menú)\n> ").strip()
        if entrada == "0":
            return None
        for dia in cartelera:
            if sin_acentos(dia) == sin_acentos(entrada):
                return dia
        print("Ese día no existe, escríbalo como aparece en la lista.")
 
 
def mostrar_funciones_del_dia(dia):
    print("\nFunciones del", dia)
    print("-" * 60)
    for f in cartelera[dia]:
        print("Sala", f["sala"], "|", f["horario"], "|", f["formato"], "|", f["pelicula"])
 
 
def pedir_funcion(dia):
    mostrar_funciones_del_dia(dia)
    while True:
        sala = input("\nElija la sala (1, 2, 3, 4 o 5. Ejemplo: 4. Escriba 0 para volver): ").strip()
        if sala == "0":
            return None
        if not sala.isdecimal():
            print("La sala debe ser un número.")
            continue
        opciones = []
        for f in cartelera[dia]:
            if f["sala"] == int(sala):
                opciones.append(f)
        if len(opciones) == 0:
            print("Esa sala no tiene función el", dia + ".")
            continue
        if len(opciones) == 1:
            f = opciones[0]
            print("Horario seleccionado:", f["horario"], "|", f["formato"], "|", f["pelicula"])
            return f
        print("\nHorarios disponibles en la sala", sala)
        for i in range(len(opciones)):
            print(str(i + 1) + ".", opciones[i]["horario"], "|", opciones[i]["formato"], "|", opciones[i]["pelicula"])
        while True:
            eleccion = input("Elija el horario por su número (Ejemplo: 1. Escriba 0 para volver): ").strip()
            if eleccion == "0":
                return None
            if eleccion.isdecimal() and 1 <= int(eleccion) <= len(opciones):
                return opciones[int(eleccion) - 1]
            print("Opción inválida.")
 
 
def pedir_asiento():
    while True:
        asiento = input("\nAsiento, fila A-E y número 1-6 (Ejemplo: C3. Escriba 0 para volver): ").strip().upper()
        if asiento == "0":
            return None
        if len(asiento) < 2 or asiento[0] not in LETRAS or not asiento[1:].isdecimal():
            print("Asiento inválido, use una letra de la A a la E y un número del 1 al 6.")
            continue
        columna = int(asiento[1:]) - 1
        if columna < 0 or columna >= COLUMNAS:
            print("Ese asiento no existe en la sala.")
            continue
        fila = LETRAS.index(asiento[0])
        asiento = asiento[0] + str(columna + 1)
        return asiento, fila, columna
 
 
def pedir_nombre():
    while True:
        nombre = input("\nNombre de quien reserva (Ejemplo: Juan Pérez): ").strip()
        if nombre != "":
            return nombre
        print("Debe escribir un nombre.")
 
 
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
 
 
def ver_cartelera():
    dia = pedir_dia()
    if dia is None:
        return
    mostrar_funciones_del_dia(dia)
 
 
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
    clave = hacer_clave(dia, funcion)
    if contar_ocupados(clave) == FILAS * COLUMNAS:
        print("\nEsta función está llena, no quedan asientos.")
        return
    mostrar_matriz(dia, funcion)
    while True:
        datos = pedir_asiento()
        if datos is None:
            return
        asiento, fila, columna = datos
        if asientos[clave][fila][columna] == "X":
            print("Ese asiento ya está ocupado, elija otro.")
        else:
            break
    nombre = pedir_nombre()
    asientos[clave][fila][columna] = "X"
    nombres[clave + "-" + asiento] = nombre
    print("\nReserva confirmada!")
    print("Nombre:", nombre)
    print("Película:", funcion["pelicula"], "(" + funcion["formato"] + ")")
    print("Día:", dia, "| Sala", funcion["sala"], "|", funcion["horario"])
    print("Asiento:", asiento)
    mostrar_matriz(dia, funcion)
 
 
def cancelar():
    dia = pedir_dia()
    if dia is None:
        return
    funcion = pedir_funcion(dia)
    if funcion is None:
        return
    clave = hacer_clave(dia, funcion)
    if contar_ocupados(clave) == 0:
        print("\nNo hay reservas en esta función, no hay nada que cancelar.")
        return
    mostrar_matriz(dia, funcion)
    while True:
        datos = pedir_asiento()
        if datos is None:
            return
        asiento, fila, columna = datos
        if asientos[clave][fila][columna] == ".":
            print("Ese asiento no está reservado, elija uno marcado con X.")
        else:
            break
    asientos[clave][fila][columna] = "."
    llave = clave + "-" + asiento
    nombre = nombres.get(llave, "")
    if llave in nombres:
        del nombres[llave]
    print("\nReserva cancelada.")
    print("Asiento:", asiento, "| Nombre:", nombre)
    mostrar_matriz(dia, funcion)
 
 
def ver_disponibilidad():
    dia = pedir_dia()
    if dia is None:
        return
    print("\nDisponibilidad del", dia)
    print("-" * 60)
    total = FILAS * COLUMNAS
    for f in cartelera[dia]:
        ocupados = contar_ocupados(hacer_clave(dia, f))
        libres = total - ocupados
        porcentaje = ocupados / total * 100
        print("Sala", f["sala"], "|", f["horario"], "|", f["formato"], "|", f["pelicula"])
        print("   Libres:", libres, "| Ocupados:", ocupados, "| Ocupación:", round(porcentaje), "%")
 
 
def seguir():
    while True:
        respuesta = input("\n¿Desea realizar otra opción? (Si o No. Ejemplo: Si): ").strip().lower()
        if respuesta == "si" or respuesta == "sí":
            return True
        elif respuesta == "no":
            return False
        else:
            print("Respuesta inválida, escriba Si o No.")
 
 
def menu():
    while True:
        print("\n===== CineMax - Sistema de Reservas =====")
        print("1. Ver cartelera de un día")
        print("2. Mostrar asientos de una función")
        print("3. Reservar asiento")
        print("4. Cancelar reserva")
        print("5. Ver disponibilidad")
        print("6. Salir")
        opcion = input("Seleccione una opción (1, 2, 3, 4, 5 o 6. Ejemplo: 3): ").strip()
 
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
            print("Opción inválida, intente de nuevo.")
            continue
 
        if not seguir():
            print("Gracias por usar CineMax!")
            break
 
 
menu()