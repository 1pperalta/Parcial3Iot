import numpy as np

def limpiar_datos(df):
    df['valor'] = df['valor'].replace(-999.0, np.nan)
    return df.dropna(subset=['valor'])