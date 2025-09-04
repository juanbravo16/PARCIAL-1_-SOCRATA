from src.api import obtener_datos
from src.ui import pedir_datos_usuario, mostrar_datos, preguntar_otro

if __name__ == "__main__":
    while True:
        departamento, limite = pedir_datos_usuario()
        df = obtener_datos(departamento, limite)
        mostrar_datos(df)

        if not preguntar_otro():
            break
