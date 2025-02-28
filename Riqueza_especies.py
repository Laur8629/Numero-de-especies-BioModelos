import os
import glob
import rasterio
import numpy as np
import fiona
from fiona.crs import from_epsg
import geopandas as gpd
from rasterio.mask import mask

def listar_tiffs(directorios):
    """Lista todos los archivos TIFF en uno o varios directorios."""
    archivos = []
    for directorio in directorios if isinstance(directorios, list) else [directorios]:
        archivos.extend(glob.glob(os.path.join(directorio, "*.tif")))
    return archivos

def leer_raster(ruta):
    """Lee un archivo raster y devuelve su matriz de datos y metadatos."""
    try:
        src = rasterio.open(ruta)  # Abre el raster sin cerrarlo automáticamente
        datos = src.read(1)
        meta = src.meta
        return datos, meta, src  # Devuelve src sin cerrarlo
    except Exception as e:
        raise ValueError(f"Error al leer el archivo {ruta}: {e}")

def verificar_y_transformar_crs_shapefile(ruta_shp):
    """Verifica si el shapefile está en EPSG:4326. Si no, lo transforma y guarda una copia en una carpeta separada."""
    try:
        gdf = gpd.read_file(ruta_shp)
        if gdf.crs is None or gdf.crs.to_epsg() != 4326:
            print(f"El shapefile {ruta_shp} no está en EPSG:4326. Transformando...")
            gdf = gdf.to_crs(epsg=4326)
            carpeta_salida = os.path.join(os.path.dirname(ruta_shp), "shapefiles_transformados")
            os.makedirs(carpeta_salida, exist_ok=True)
            ruta_transformada = os.path.join(carpeta_salida, os.path.basename(ruta_shp))
            gdf.to_file(ruta_transformada)
            print(f"Shapefile transformado guardado en: {ruta_transformada}")
            return ruta_transformada
        else:
            print(f"El shapefile {ruta_shp} ya está en EPSG:4326.")
            return ruta_shp
    except Exception as e:
        raise ValueError(f"Error al verificar/transformar el CRS del shapefile {ruta_shp}: {e}")

def limpiar_nombres_tiffs(lista_tiffs):
    """Limpia los nombres de los archivos TIFF eliminando sufijos no deseados y caracteres especiales."""
    species_names = set()
    for nombre_archivo in lista_tiffs:
        nombre_limpio = nombre_archivo.replace('_10_MAXENT.tif', '').replace('_veg.tif', '').replace('_pub.tif', '').replace('_con.tif', '').replace('_exp.tif', '').replace('.tif', '').replace('_pub1', ' ').replace('_', ' ')
        species_names.add(nombre_limpio)
    return sorted(species_names)

def especies_en_area(directorios, shapefile):
    """Devuelve cuántas y cuáles especies tienen distribución en el área del polígono del shapefile."""
    especies_presentes = []
    archivos_problematicos = []
    archivos = listar_tiffs(directorios)
    
    if not archivos:
        raise FileNotFoundError("No se encontraron archivos TIFF en los directorios proporcionados.")
    
    with fiona.open(shapefile, "r") as shapefile_f:
        shapes = [feature["geometry"] for feature in shapefile_f]
    
    for archivo in archivos:
        datos, meta, src = leer_raster(archivo)  # Abre el raster
        
        try:
            out_image, _ = mask(src, shapes, crop=True)  # Usa el raster abierto
            if np.any(out_image > 0):  # Si hay valores positivos en el área
                especies_presentes.append(os.path.basename(archivo))
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")
            archivos_problematicos.append(os.path.basename(archivo))
        finally:
            src.close()  # Cierra el raster después de usarlo
    
    especies_presentes = limpiar_nombres_tiffs(especies_presentes)
    
    if archivos_problematicos:
        return len(especies_presentes), especies_presentes, archivos_problematicos
    else:
        return len(especies_presentes), especies_presentes

if __name__ == "__main__":
    directorios = ["C:/Users/laura/OneDrive - Universidad de los andes/Escritorio/HUMBOLDT/Carnivoros/modelos carnivoros/n2/"]  # Lista de directorios con archivos TIFF, de ser solo uno colocar la unica ruta
    shapefile = "C:/Users/laura/OneDrive - Universidad de los andes/Escritorio/HUMBOLDT/FPV/especies biomodelos FPV/Nucleo_Desarrollo_Forestal - Bibiana Gómez Valencia/Nucleo_Desarrollo_Forestal.shp"
    
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
