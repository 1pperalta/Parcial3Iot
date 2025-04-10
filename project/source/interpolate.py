import numpy as np
import pandas as pd
import pydeck as pdk
from scipy.interpolate import griddata

def crear_heatmap_nozero(df, grid_size=200, radius_pixels=30, intensity=0.6, threshold=0.05):
    # Filtrar para solo tener datos con valor > 0
    df = df[df["valor"] > 0].dropna(subset=["latitud", "longitud", "valor"]).copy()
    if df.empty:
        return None
    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    
    lat_min, lat_max = df["latitud"].min(), df["latitud"].max()
    lon_min, lon_max = df["longitud"].min(), df["longitud"].max()
    if lat_min == lat_max or lon_min == lon_max:
        return None
    
    grid_lon, grid_lat = np.mgrid[lon_min:lon_max:complex(grid_size), lat_min:lat_max:complex(grid_size)]
    puntos = df[["longitud", "latitud"]].values
    valores = df["valor"].values
    grid_vals = griddata(puntos, valores, (grid_lon, grid_lat), method="nearest")
    
    df_grid = pd.DataFrame({
        "lon": grid_lon.ravel(),
        "lat": grid_lat.ravel(),
        "valor": grid_vals.ravel()
    })
    
    vista = pdk.ViewState(
        latitude=df["latitud"].mean(),
        longitude=df["longitud"].mean(),
        zoom=10
    )
    
    return pdk.Deck(
        layers=[pdk.Layer("HeatmapLayer",
                          data=df_grid,
                          get_position='[lon, lat]',
                          get_weight="valor",
                          radius_pixels=radius_pixels,
                          intensity=intensity,
                          threshold=threshold)],
        initial_view_state=vista,
        map_style="mapbox://styles/mapbox/light-v9"
    )
