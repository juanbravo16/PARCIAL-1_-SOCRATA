from sodapy import Socrata
import pandas as pd

def obtener_datos(departamento: str = None, limite: int = 100) -> pd.DataFrame:
    """
    Trae datos del dataset gt2j-8ykr.
    Si 'departamento' está dado, filtra usando una comparación case-insensitive.
    Devuelve un DataFrame con las columnas disponibles entre las solicitadas.
    """
    client = Socrata("www.datos.gov.co", None)

    # Construir la consulta (usamos where para comparacion en mayusculas)
    try:
        if departamento and departamento.strip() != "":
            dept = departamento.strip().upper()
            where_clause = f"upper(departamento_nom) = '{dept}'"
            resultados = client.get("gt2j-8ykr", where=where_clause, limit=limite)
        else:
            resultados = client.get("gt2j-8ykr", limit=limite)
    except Exception as e:
        # Re-levantar el error para que el caller lo vea (puedes manejarlo desde main)
        raise

    df = pd.DataFrame.from_records(resultados)

    # Si viene vacío lo devolvemos (main puede decidir qué mostrar)
    if df.empty:
        return df

    # Columnas que queremos mostrar (intento principal)
    deseadas = [
        "ciudad_municipio_nom",
        "departamento_nom",
        "edad",
        "fuente_tipo_contagio",
        "estado",
        "pais_viajo_1_nom"
    ]

    # Intersección simple (solo las columnas que realmente existen)
    existentes = [c for c in deseadas if c in df.columns]

    # Si no encontramos ninguna, intentamos con nombres alternativos comunes
    if not existentes:
        alternativas = {
            "ciudad_municipio_nom": ["ciudad_municipio_nom", "ciudad_municipio", "ciudad_de_ubicacion", "ciudad_de_ubicaci_n"],
            "departamento_nom": ["departamento_nom", "departamento"],
            "edad": ["edad"],
            "fuente_tipo_contagio": ["fuente_tipo_contagio", "tipo"],
            "estado": ["estado"],
            "pais_viajo_1_nom": ["pais_viajo_1_nom", "pais_viajo_1", "pais"]
        }
        for key, cand_list in alternativas.items():
            for cand in cand_list:
                if cand in df.columns and cand not in existentes:
                    existentes.append(cand)
                    break

    # Si aún no hay columnas coincidentes, devolvemos el df completo para inspección
    if not existentes:
        return df

    # Seleccionamos solo las columnas existentes y las renombramos a algo amigable
    df_sel = df.loc[:, existentes].copy()
    rename_map = {
        "ciudad_municipio_nom": "Ciudad",
        "ciudad_municipio": "Ciudad",
        "departamento_nom": "Departamento",
        "departamento": "Departamento",
        "edad": "Edad",
        "fuente_tipo_contagio": "Tipo",
        "tipo": "Tipo",
        "estado": "Estado",
        "pais_viajo_1_nom": "Pais_Procedencia",
        "pais_viajo_1": "Pais_Procedencia",
        "pais": "Pais_Procedencia"
    }
    df_sel.rename(columns={c: rename_map.get(c, c) for c in df_sel.columns}, inplace=True)

    return df_sel
