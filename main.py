from flask import Flask, render_template
import pandas as pd
import folium

app = Flask(__name__)

@app.route('/')
def home():
    try:
        file_path = 'data/Ramsar_sites.csv'
        df = pd.read_csv(file_path, delimiter=',', quotechar='"')

        #Definción de elementos
        df['Latitude'] = df['Latitude'].apply(lambda x: dms_to_dd(x))
        df['Longitude'] = df['Longitude'].apply(lambda x: dms_to_dd(x))
        df = df.dropna(subset=['Latitude', 'Longitude'])
        df_colombia = df[df['Country'] == 'Colombia']
        m = folium.Map(location=[4.5, -74.0], zoom_start=6)

        #Crea capa de estilo
        folium.TileLayer(
            tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
            attr='© OpenStreetMap contributors © CartoDB',
            name='CartoDB Positron'
        ).add_to(m)

        #Crea capa de elementos
        wetland_layer = folium.FeatureGroup(name='Humedales Colombianos')

        def get_color(name):
            if "Complejo" in name:
                return 'blue'
            elif "Sistema" in name:
                return 'green'
            else:
                return 'red'

        #Crea los marcadores de cada humedal
        for _, row in df_colombia.iterrows():
            color = get_color(row['Site name'])
            popup_info = f"""
            <b>{row['Site name']}</b><br>
            <button onclick="parent.showWetlandInfo('{row['Site name']}', '{row['Territory']}', '{row['Designation date']}', '{row['Area (ha)']}', '{row['Annotated summary']}', '{row['Latitude']}', '{row['Longitude']}')">Ver Información</button>
            """
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_info, max_width=225),
                icon=folium.Icon(color=color)
            ).add_to(wetland_layer)

        # Añade pas de elementos y estilo
        wetland_layer.add_to(m)
        folium.LayerControl().add_to(m)
        # Crea map.html
        map_path = 'static/map.html'
        m.save(map_path)

        # Perpara los datos a pasar
        wetlands_info = df_colombia.to_dict(orient='records')

    except Exception as e:
        return f"Error: {e}"

    return render_template('index.html', wetlands_info=wetlands_info)

def dms_to_dd(dms):
    try:
        if isinstance(dms, float):
            return dms
        #Pasa las coordenadas geograficas a cartecianas
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
