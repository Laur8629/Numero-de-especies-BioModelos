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

## Cruzar Especies con una Base de Datos

### Función `cruzar_con_base_datos`
La función `cruzar_con_base_datos` permite comparar la lista de especies detectadas en el área con una base de datos externa en formato CSV o TSV. De esta manera, se pueden obtener datos adicionales como categorías de amenaza, endemismo, inclusión en CITES, entre otros.

### Parámetros:
- `lista_especies (list)`: Lista de nombres de especies presentes en el área.
- `ruta_base_datos (str)`: Ruta al archivo CSV o TSV que contiene la información adicional de las especies.
- `ruta_salida (str, opcional)`: Carpeta donde se guardará el archivo de salida.
- `separador (str)`: Separador del archivo de entrada (por defecto `","` para CSV, o `"\t"` para TSV).

### Funcionamiento:
1. Carga la base de datos desde la ruta indicada.
2. Detecta automáticamente la columna que contiene los nombres de las especies.
3. Filtra las especies presentes en el área.
4. Guarda el resultado en un nuevo archivo llamado `especies_por_categoria.csv` en la carpeta especificada (o en el directorio actual si no se proporciona ruta de salida).

### Uso en el código principal:
Después de ejecutar `especies_en_area()`, se puede realizar el cruce con la base de datos de la siguiente manera:

```python
num_especies, lista_especies = resultado[:2]
base_datos_csv = "C:/ruta/a/tu/base_de_datos.csv"  # Archivo con información adicional
ruta_salida = "C:/ruta/de/salida/"  # Carpeta donde guardar el resultado

df_especies_con_categorias = cruzar_con_base_datos(lista_especies, base_datos_csv, ruta_salida)

if df_especies_con_categorias is not None:
    print("\n✅ Cruce realizado con éxito. Revisa el archivo generado.")
```

### Archivo de salida:
El archivo generado, `especies_por_categoria.csv`, contendrá únicamente las especies presentes en el área junto con la información adicional encontrada en la base de datos.



