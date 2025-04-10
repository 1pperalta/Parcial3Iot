import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pydeck as pdk
import pandas as pd

from source.extract import extraer_datos
from source.clean import limpiar_datos
from source.transform import transformar_datos
from source.interpolate import crear_heatmap_nozero# Importa la función con geopy

def get_color(clasificacion):
    """
    Asigna un color en formato RGBA basado en la clasificación:
      - "sin lluvia": verde
      - "llovizna" o "lluvia ligera": azul
      - "lluvia moderada": naranja
      - "lluvia intensa" o "lluvia muy intensa": rojo
      - Cualquier otra: gris
    """
    if clasificacion == "sin lluvia":
        return [0, 200, 0, 160]
    elif clasificacion in ["llovizna", "lluvia ligera"]:
        return [5, 122, 240, 160]
    elif clasificacion == "lluvia moderada":
        return [255, 165, 0, 160]
    elif clasificacion in ["lluvia intensa", "lluvia muy intensa"]:
        return [255, 0, 0, 160]
    else:
        return [200, 200, 200, 160]

def main():
    # Configurar autorefresco vía sidebar
    refresh_interval = st.sidebar.number_input("Intervalo de actualización (segundos)", min_value=10, value=60)
    st.sidebar.write(f"La aplicación se recargará automáticamente cada {refresh_interval} segundos.")
    st_autorefresh(interval=refresh_interval * 1000, key="refresher")
    
    st.title("Dashboard Pluviométrico en Tiempo Real")
    st.write("Extracción, limpieza, transformación e interpolación de datos de SIATA")
    
    # Extracción de datos
    try:
        df = extraer_datos()
    except Exception as e:
        st.error(f"Error al extraer datos: {e}")
        return
    
    # Limpieza y transformación
    df = limpiar_datos(df)
    df = transformar_datos(df)
    
    st.subheader("Datos Procesados")
    st.dataframe(df)
    
    st.image("leyenda_colores.png", use_container_width=True, caption="Interpretación de los colores en el mapa")
    
    # Mapa interactivo de sensores (Scatterplot)
    if 'latitud' in df.columns and 'longitud' in df.columns and 'clasificacion' in df.columns:
        df_map = df.copy()
        df_map['latitud'] = pd.to_numeric(df_map['latitud'], errors='coerce')
        df_map['longitud'] = pd.to_numeric(df_map['longitud'], errors='coerce')
        df_map = df_map.dropna(subset=['latitud', 'longitud'])
        df_map = df_map.rename(columns={"latitud": "lat", "longitud": "lon"})
        df_map["color"] = df_map["clasificacion"].apply(lambda x: get_color(x))
    
        st.subheader("Mapa Interactivo de Sensores (con borde negro)")
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_map,
            get_position="[lon, lat]",
            get_color="color",
            get_radius=100,
            pickable=True,
            get_line_color=[0, 0, 0, 255],
            line_width_min_pixels=2,
        )
    
        view_state = pdk.ViewState(
            latitude=df_map["lat"].mean(),
            longitude=df_map["lon"].mean(),
            zoom=10,
            pitch=0,
        )
    
        scatter_deck = pdk.Deck(
            layers=[scatter_layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/light-v9",
            tooltip={"text": "Clasificación: {clasificacion}"}
        )
    
        st.pydeck_chart(scatter_deck)
    else:
        st.write("No se dispone de datos completos (latitud, longitud y clasificación) para el mapa interactivo.")
    
    heatmap = crear_heatmap_nozero(df)
    if heatmap:
        st.pydeck_chart(heatmap)
    else:
        st.warning("No se encontró lluvia (valores > 0) para generar el heatmap.")

if __name__ == "__main__":
    main()
