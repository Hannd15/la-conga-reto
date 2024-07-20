from flask import Flask, render_template
import pandas as pd
import folium
import geopandas as gpd
from shapely.geometry import Point

app = Flask(__name__)

# Función para convertir coordenadas DMS a decimales
def dms_to_dd(dms):
    try:
        if isinstance(dms, float):
            return dms
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

# Ruta principal
@app.route('/')
def home():
    try:
        # Carga de datos
        file_path = 'data/Ramsar_sites.csv'
        df = pd.read_csv(file_path, delimiter=',', quotechar='"')
        df['Latitude'] = df['Latitude'].apply(lambda x: dms_to_dd(x))
        df['Longitude'] = df['Longitude'].apply(lambda x: dms_to_dd(x))
        df_colombia = df.dropna(subset=['Latitude', 'Longitude'])

        # Carga de zonas de protección ambiental
        proteccion_ambiental_path = 'data/Parques_Nacionales_Naturales_de_Colombia.shp'
        gdf_national_parks = gpd.read_file(proteccion_ambiental_path)

        # Conversión a GeoDataFrame
        gdf_wetlands = gpd.GeoDataFrame(df_colombia, geometry=gpd.points_from_xy(df_colombia.Longitude, df_colombia.Latitude))

        # Intersección espacial
        protected_wetlands = gpd.sjoin(gdf_wetlands, gdf_national_parks, how='inner', predicate='intersects')
        
        # Encuentra los humedales fuera de zonas protegidas
        unprotected_wetlands = gdf_wetlands[~gdf_wetlands.index.isin(protected_wetlands.index)]

        # Mapa
        m = folium.Map(location=[4.5, -74.0], zoom_start=6)
        folium.TileLayer(tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', attr='© OpenStreetMap contributors © CartoDB', name='CartoDB Positron').add_to(m)

        # Capa de humedales
        protected_layer = folium.FeatureGroup(name='Humedales en zonas de protección ambiental')
        not_protected_layer = folium.FeatureGroup(name='Humedales fuera de zonas de protección ambiental')

        # Función para definir color de los marcadores
        def get_color(name):
            if "Complejo" in name:
                return 'blue'
            elif "Sistema" in name:
                return 'green'
            else:
                return 'red'



        # Marcadores protegidos
        for _, row in protected_wetlands.iterrows():
            color = get_color(row['Site name'])
            popup_info = f"""
            <b>{row['Site name']}</b><br>
            <button onclick="parent.showWetlandInfo('{row['Site name']}', '{row['Territory']}', '{row['Designation date']}', '{row['Area (ha)']}', '{row['Annotated summary']}', '{row['Latitude']}', '{row['Longitude']}', '{row['Threats']}', '{row['Ramsar Site No.']}')">Ver Información</button>
            """
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_info, max_width=225),
                icon=folium.Icon(color=color)
            ).add_to(protected_layer)

        # Marcadores no protegidos
        for _, row in unprotected_wetlands.iterrows():
            color = get_color(row['Site name'])
            popup_info = f"""
            <b>{row['Site name']}</b><br>
            <button onclick="parent.showWetlandInfo('{row['Site name']}', '{row['Territory']}', '{row['Designation date']}', '{row['Area (ha)']}', '{row['Annotated summary']}', '{row['Latitude']}', '{row['Longitude']}', '{row['Threats']}', '{row['Ramsar Site No.']}')">Ver Información</button>
            """
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_info, max_width=225),
                icon=folium.Icon(color=color)
            ).add_to(not_protected_layer)

        # Añade capa de elementos y estilo
        protected_layer.add_to(m)
        not_protected_layer.add_to(m)
        folium.LayerControl().add_to(m)

        # Guarda el mapa
        map_path = 'static/map.html'
        m.save(map_path)

        # Prepara los datos a pasar
        wetlands_info = df_colombia.to_dict(orient='records')

    except Exception as e:
        return f"Error: {e}"

    return render_template('index.html', wetlands_info=wetlands_info)

if __name__ == '__main__':
    app.run(debug=True)
