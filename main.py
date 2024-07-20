from flask import Flask, render_template
import pandas as pd
import folium
from shapely.geometry import Point
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Leer el archivo CSV con coma como delimitador y manejar las comillas correctamente
        file_path = 'data/humedales_colombia.csv'
        df = pd.read_csv(file_path, delimiter=',', quotechar='"')

        # Convertir las coordenadas a formato decimal
        df['Latitude'] = df['Latitude'].apply(lambda x: dms_to_dd(x))
        df['Longitude'] = df['Longitude'].apply(lambda x: dms_to_dd(x))

        # Filtrar filas con valores NaN en las columnas de latitud o longitud
        df = df.dropna(subset=['Latitude', 'Longitude'])

        # Filtrar los datos para mantener solo los que están en Colombia
        df_colombia = df[df['Country'] == 'Colombia']

        # Crear el mapa base de Folium
        m = folium.Map(location=[4.5, -74.0], zoom_start=6)

        # Añadir puntos al mapa
        for _, row in df_colombia.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"{row['Site name']}<br>Region: {row['Region']}<br>Size: {row['Area (ha)']} ha",
                icon=folium.Icon(color='red')
            ).add_to(m)

        # Crear la carpeta 'templates' si no existe
        if not os.path.exists('templates'):
            os.makedirs('templates')

        # Guardar el mapa en un archivo HTML
        map_path = 'templates/map.html'
        m.save(map_path)

    except Exception as e:
        return f"Error: {e}"

    return render_template('map.html')

# Función para convertir DMS a decimal
def dms_to_dd(dms):
    try:
        # Si el valor ya es un número flotante, retornarlo directamente
        if isinstance(dms, float):
            return dms
        
        # Si el valor es una cadena, proceder con la conversión
        if isinstance(dms, str):
            dms = dms.replace('°', ' ').replace('\'', ' ').replace('\"', ' ').split()
            if len(dms) < 3:
                raise ValueError(f"El valor '{dms}' no tiene suficientes partes para la conversión.")
            d = float(dms[0])
            m = float(dms[1])
            s = float(dms[2])
            direction = dms[3]
            dd = d + m / 60 + s / 3600
            if direction in ['S', 'W']:
                dd *= -1
            return dd
        else:
            raise ValueError(f"El valor '{dms}' no es un string válido para la conversión.")
    except Exception as e:
        raise ValueError(f"Error en la conversión de DMS a decimal: {e}")

if __name__ == '__main__':
    app.run(debug=True)