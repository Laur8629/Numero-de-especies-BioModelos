# Identificación de Especies en un Área de Estudio

Este script permite identificar qué especies (representadas como archivos **TIFF**) están presentes en un área de interés definida por un **shapefile**.  
Adicionalmente, permite **cruzar los resultados** con una base de datos externa en formato CSV o TSV.

---

## 📂 Estructura del Proyecto

```
numero_especies_biomodelos/
│
├── numero_especies.py    # Script principal
├── README.md             # Este archivo
└── data/                 # Carpeta sugerida para guardar insumos y salidas
```

---

## ⚙️ Dependencias

El script requiere **Python 3.8+** y las siguientes librerías:

- numpy  
- pandas  
- rasterio  
- geopandas  
- fiona  

Puedes instalarlas con:

```bash
pip install numpy pandas rasterio geopandas fiona
```

---

## 🔧 Configuración de Rutas

Al inicio del archivo `species_richness.py` hay una sección para ajustar las rutas según tu caso:

```python
# ======================== CONFIGURACIÓN DE RUTAS ======================== #
directorios = ["/ruta/a/carpeta/con/archivos/"]   # Carpetas con archivos .tif
shapefile = "/ruta/a/shapefile/area_estudio.shp"  # Shapefile del área de estudio
ruta_salida = "/ruta/a/guardar/listado_especies.csv"  # CSV con listado de especies
base_datos_csv = "/ruta/a/base_datos.csv"  # Base de datos externa opcional
# ======================================================================== #
```

🔹 **directorios**: carpeta(s) que contienen los rasters de especies (.tif)  
🔹 **shapefile**: archivo con el polígono del área de interés  
🔹 **ruta_salida**: dónde se guardará el listado de especies encontradas  
🔹 **base_datos_csv** *(opcional)*: CSV o TSV con información adicional de especies  

---

## ▶️ Ejecución

Ejecuta el script desde la terminal:

```bash
python species_richness.py
```

Al finalizar, mostrará en consola:

- Número de especies presentes  
- Listado de especies detectadas  
- Archivos problemáticos (si los hay)  

Además, generará:

- `listado_especies.csv`: archivo con los nombres de las especies encontradas  
- `especies_por_categoria.csv`: (si se proporciona una base de datos) cruce con datos adicionales  

---

## 📊 Ejemplo de Salida en Consola

```
Número de especies presentes en el área: 15
Especies presentes: ['Atelopus ignescens', 'Anolis heterodermus', 'Pleurodema brachyops']
Archivos problemáticos: ['especie_x.tif']
✅ Archivo guardado en: /ruta/a/guardar/listado_especies.csv
✅ Cruce realizado con éxito. Revisa el archivo generado.
```

---

## 📑 Notas Importantes

- El shapefile debe tener un **CRS válido**. Si no está en **EPSG:4326**, el script lo transformará automáticamente.  
- Los TIFF deben tener **valores binarios de presencia/ausencia** (o 0/1). Actualmente se asume que el valor `1` indica presencia.  
- El script no calcula riqueza real, solo identifica especies **potencialmente presentes** en el área de interés, según los píxeles de los modelos.  

---

## 📜 Licencia

Este código se distribuye bajo la licencia **MIT** para uso libre y responsable.  
Por favor, cita la fuente de los datos originales si utilizas BioModelos u otros proveedores.

---
