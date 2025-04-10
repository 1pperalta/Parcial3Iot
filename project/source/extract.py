import requests
import pandas as pd

def extraer_datos(url="https://siata.gov.co/data/siata_app/Pluviometrica.json"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        dt = response.json()
        # Normaliza la parte anidada para obtener las estaciones
        df_estaciones = pd.json_normalize(dt['estaciones'])
        return df_estaciones
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error al obtener datos: {e}")
