# Reto 11 - Reconocimiento ciudadano de las transformaciones de humedales en Colombia

Esta aplicación web muestra un mapa interactivo de humedales en Colombia, clasificándolos según su ubicación dentro o fuera de zonas de protección ambiental y permitiendo a los usuarios ver información detallada y timelapses de los humedales.

## Funcionalidades

- Muestra un mapa interactivo con los humedales de Colombia.
- Clasifica humedales según su ubicación en zonas de protección ambiental.
- Permite a los usuarios ver información de cada humedal como su tamaño y factores de riesgo.
- Muestra timelapses mostrando el estado de cada humedal desde 1984 hasta 2022.

## Archivos y Directorios

- `main.py`: Archivo principal de la aplicación Flask.
- `data/`: Contiene los archivos de datos, incluyendo los sitios Ramsar y las zonas de protección ambiental.
- `templates/`: Contiene las plantillas HTML para la aplicación.
- `static/`: Contiene archivos estáticos como el mapa generado y archivos CSS.
- `requirements.txt`: Lista de dependencias del proyecto.
- `README.md`: Este archivo.

## Configuración y Ejecución

### Prerrequisitos

Asegúrate de tener Python 3 y pip instalados en tu sistema.

### Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/Hannd15/la-conga-reto
    cd la-conga-reto
    ```

2. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

### Ejecución

1. Ejecuta la aplicación:
    ```sh
    python main.py
    ```

2. Abre tu navegador y navega a `http://127.0.0.1:5000/` para ver la aplicación.

## Descripción de Funciones

### Mapa Interactivo

Utiliza Folium para generar un mapa interactivo que clasifica los humedales en dos capas:
- Humedales en zonas de protección ambiental.
- Humedales fuera de zonas de protección ambiental.

### Timelapses

Los timelapses se embebeden de Google Earth Engine usando su API y se enfocan en la ubicación del humedal seleccionado.

### Información relevante

Se usan los datos provistos por los sitios Ramsar y se traducen del inglés al español para permitir una mejor accesibilidad.

### Traductor

La traducción se realiza en una máquina virtual en la nube ejecutando el servicio de traducción [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate).
