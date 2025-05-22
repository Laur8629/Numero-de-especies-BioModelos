"""
Este script identifica qué especies (representadas como archivos TIFF) están presentes en un área definida por un shapefile.
También convierte el shapefile a EPSG:4326 si es necesario, reproyecta los TIFFs si tienen otro CRS, y guarda un listado con las especies encontradas.
"""

import os
import glob
import rasterio
import numpy as np
import fiona
import geopandas as gpd
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling
from gdal import MemoryFile


def listar_tiffs(directorios):
    """Recorre uno o varios directorios y lista todos los archivos .tif encontrados."""
    archivos = []
    for directorio in directorios if isinstance(directorios, list) else [directorios]:
        archivos.extend(glob.glob(os.path.join(directorio, "*.tif")))
    return archivos


def leer_raster(ruta):
    """Abre un archivo raster y retorna los datos, metadatos y el objeto rasterio."""
    try:
        src = rasterio.open(ruta)
        datos = src.read(1)
        meta = src.meta
        return datos, meta, src
    except Exception as e:
        raise ValueError(f"Error al leer el archivo {ruta}: {e}")


def reproyectar_raster(src, destino_crs='EPSG:4326'):
    """Reproyecta un archivo raster a EPSG:4326."""
    transform, width, height = calculate_default_transform(
        src.crs, destino_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': destino_crs,
        'transform': transform,
        'width': width,
        'height': height
    })
    
    memfile = rasterio.io.MemoryFile()
    dst = memfile.open(**kwargs)
    for i in range(1, src.count + 1):
        reproject(
            source=rasterio.band(src, i),
            destination=rasterio.band(dst, i),
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=destino_crs,
            resampling=Resampling.nearest
        )
    return dst


def verificar_y_transformar_crs_shapefile(ruta_shp):
    """Verifica si el shapefile está en EPSG:4326 y lo transforma si es necesario."""
    try:
        gdf = gpd.read_file(ruta_shp)
        if gdf.crs is None or gdf.crs.to_epsg() != 4326:
            print(f"Transformando el shapefile {ruta_shp} a EPSG:4326...")
            gdf = gdf.to_crs(epsg=4326)
            carpeta_salida = os.path.join(os.path.dirname(ruta_shp), "shapefiles_transformados")
            os.makedirs(carpeta_salida, exist_ok=True)
            ruta_transformada = os.path.join(carpeta_salida, os.path.basename(ruta_shp))
            gdf.to_file(ruta_transformada)
            return ruta_transformada
        else:
            return ruta_shp
    except Exception as e:
        raise ValueError(f"Error al procesar el CRS del shapefile {ruta_shp}: {e}")


def limpiar_nombres_tiffs(lista_tiffs):
    """Limpia los nombres de los archivos TIFF para obtener los nombres de especies."""
    species_names = set()
    for nombre_archivo in lista_tiffs:
        nombre_limpio = os.path.basename(nombre_archivo)
        for sufijo in ['_10_MAXENT.tif', '_veg.tif', '_pub.tif', '_con.tif', '_exp.tif', '.tif']:
            nombre_limpio = nombre_limpio.replace(sufijo, '')
        nombre_limpio = nombre_limpio.replace('_pub1', ' ').replace('_', ' ')
        species_names.add(nombre_limpio)
    return sorted(species_names)


def especies_en_area(directorios, shapefile):
    """Evalúa qué especies están presentes en el área del shapefile."""
    especies_presentes = []
    archivos_problematicos = []
    archivos = listar_tiffs(directorios)
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos TIFF en los directorios proporcionados.")

    with fiona.open(shapefile, "r") as shapefile_f:
        shapes = [feature["geometry"] for feature in shapefile_f]

    for archivo in archivos:
        datos, meta, src = leer_raster(archivo)
        try:
            if src.crs.to_string() != 'EPSG:4326':
                dst = reproyectar_raster(src)
                out_image, _ = mask(dst, shapes, crop=True)
                dst.close()
            else:
                out_image, _ = mask(src, shapes, crop=True)
            if np.any(out_image == 1):
                especies_presentes.append(archivo)
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
            archivos_problematicos.append(archivo)
        finally:
            src.close()

    especies_presentes = limpiar_nombres_tiffs(especies_presentes)
    if archivos_problematicos:
        return len(especies_presentes), especies_presentes, archivos_problematicos
    else:
        return len(especies_presentes), especies_presentes


if __name__ == "__main__":
    ### Rutas genéricas a reemplazar por rutas reales###
    directorios = [
        "/ruta/a/carpeta/con/archivos/",
    ]
    shapefile = "/ruta/a/shapefile/area_estudio.shp"

    shapefile = verificar_y_transformar_crs_shapefile(shapefile)
    resultado = especies_en_area(directorios, shapefile)

    if len(resultado) == 3:
        num_especies, lista_especies, archivos_problematicos = resultado
        print(f"Número de especies presentes en el área: {num_especies}")
        print("Especies presentes:", lista_especies)
        print("Archivos problemáticos:", archivos_problematicos)
    else:
        num_especies, lista_especies = resultado
        print(f"Número de especies presentes en el área: {num_especies}")
        print("Especies presentes:", lista_especies)

    # Guardar resultados en CSV
    import csv
    ruta_salida = "/ruta/a/guardar/listado_especies.csv" #Especificar ruta de salida
    with open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['Especie'])
        for especie in lista_especies:
            escritor.writerow([especie])


#### Cruzar con la base de datos###

    import pandas as pd
import os

def cruzar_con_base_datos(lista_especies, ruta_base_datos, ruta_salida=None, separador=","):
    """
    Cruza la lista de especies presentes en el área con una base de datos en CSV o TSV.
    
    Parámetros:
    - lista_especies (list): Lista de nombres de especies presentes en el área.
    - ruta_base_datos (str): Ruta al archivo CSV o TSV con información adicional de especies.
    - ruta_salida (str, opcional): Ruta del directorio donde se guardará el archivo resultado.
    - separador (str): Separador del archivo ("," para CSV, "\t" para TSV).
    
    Retorna:
    - Un DataFrame con las especies filtradas y sus datos adicionales.
    """
    try:
        # Cargar la base de datos
        df = pd.read_csv(ruta_base_datos, sep=separador, dtype=str)

        # Buscar la columna que contiene los nombres de las especies
        columna_especies = None
        for col in df.columns:
            if "especie" in col.lower() or "nombre_cientifico" in col.lower():
                columna_especies = col
                break

        if columna_especies is None:
            raise ValueError("No se encontró una columna con el nombre de la especie en la base de datos.")

        # Filtrar las especies presentes en el área
        df_filtrado = df[df[columna_especies].isin(lista_especies)]

        if df_filtrado.empty:
            print("⚠️ No se encontraron coincidencias en la base de datos.")
        else:
            # Determinar la ruta de salida
            if ruta_salida is None:
                ruta_salida = os.getcwd()  # Directorio actual si no se proporciona ruta
            ruta_completa = os.path.join(ruta_salida, "especies_por_categoria.csv")

            # Guardar el archivo
            df_filtrado.to_csv(ruta_completa, index=False, sep=separador)
            print(f"✅ Archivo guardado en: {ruta_completa}")

        return df_filtrado

    except Exception as e:
        print(f"❌ Error al procesar la base de datos: {e}")
        return None

    
    df_especies_con_categorias = cruzar_con_base_datos(lista_especies, base_datos_csv, ruta_salida)

    if df_especies_con_categorias is not None:
        print("\n✅ Cruce realizado con éxito. Revisa el archivo generado.")

