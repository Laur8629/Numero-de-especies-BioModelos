# README - Análisis de Especies en Área Basado en Rasters

Este script en Python permite analizar la distribución de especies en un área geográfica definida por un shapefile. Utiliza archivos raster (TIFF) para determinar qué especies están presentes en la región de interés.

## Requisitos

Antes de ejecutar el script, asegúrese de tener instaladas las siguientes dependencias:

- Python 3.8 o superior
- rasterio
- numpy
- geopandas
- fiona
- os
- glob

Puede instalar las bibliotecas necesarias ejecutando:

```bash
pip install rasterio numpy geopandas fiona
```

## Uso

1. **Definir los directorios de entrada:** Modifique la variable `directorios` en el script con las rutas a los directorios donde se encuentran los archivos TIFF.
2. **Especificar el shapefile:** Ajuste la variable `shapefile` con la ruta al archivo shapefile que define el área de interés.
3. **Ejecutar el script desde la terminal:**

```bash
python Riqueza_especies.py
```

(Reemplace `nombre_del_script.py` con el nombre real del archivo donde guardó el código.)

## Funciones Principales

### `listar_tiffs(directorios)`
Lista todos los archivos TIFF en uno o varios directorios especificados.

### `leer_raster(ruta)`
Lee un archivo raster y devuelve su matriz de datos, metadatos y el objeto rasterio abierto.

### `verificar_y_transformar_crs_shapefile(ruta_shp)`
Verifica si el shapefile está en el sistema de referencia EPSG:4326. Si no lo está, lo transforma y guarda una copia.

### `limpiar_nombres_tiffs(lista_tiffs)`
Limpia los nombres de los archivos TIFF eliminando sufijos no deseados y caracteres especiales.

### `especies_en_area(directorios, shapefile)`
Determina qué especies tienen distribución en el área definida por el shapefile y devuelve la cantidad y lista de especies presentes.

## Salida del Programa

El script imprimirá:

- El número total de especies presentes en el área de interés.
- La lista de especies encontradas.
- (Opcional) Una lista de archivos TIFF problemáticos si los hay.

