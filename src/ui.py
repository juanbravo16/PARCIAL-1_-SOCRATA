def pedir_datos_usuario():
    dept = input("Ingrese el nombre del departamento: ")
    while True:
        try:
            limite = int(input("Ingrese el numero de registros a consultar: "))
            break
        except ValueError:
            print("Debe ingresar un numero entero.")
    return dept, limite


def mostrar_datos(df):
    if df.empty:
        print("No se encontraron datos para la consulta.")
        return
    print("\nResultados:")
    print(df.to_string(index=False))


def preguntar_otro():
    while True:
        opcion = input("\n¿Desea hacer otra consulta? (s/n): ").strip().lower()
        if opcion == "s":
            return True
        elif opcion == "n":
            print("Gracias por usar el programa. ¡Hasta luego!")
            return False
        else:
            print("Respuesta inválida, escriba 's' o 'n'.")
