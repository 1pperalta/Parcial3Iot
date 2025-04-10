def clasificar_precipitacion(valor):
    if valor == 0:
        return "sin lluvia"
    elif 0 < valor <= 2.5:
        return "llovizna"
    elif 2.5 < valor <= 7.6:
        return "lluvia ligera"
    elif 7.6 < valor <= 16.0:
        return "lluvia moderada"
    elif 16.0 < valor <= 50.0:
        return "lluvia intensa"
    elif valor > 50.0:
        return "lluvia muy intensa"
    else:
        return "dato no clasificado"

def transformar_datos(df):
    df['clasificacion'] = df['valor'].apply(clasificar_precipitacion)
    return df
