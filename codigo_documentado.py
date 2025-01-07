# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:09:14 2024

@author: laura garcia
"""

#Importar librerias
import os
import numpy as np
import rasterio
from rasterio.mask import mask
import fiona
import pandas as pd

def recortar_y_filtrar_tiffs(carpeta_tiffs, archivo_shapefile):
    # Abre el archivo shapefile y extrae la geometría de los polígonos
    with fiona.open(archivo_shapefile, 'r') as shapefile:
        geometria = [feature["geometry"] for feature in shapefile]

    # Listas para almacenar los nombres de TIFFs válidos y problemáticos
    tiffs_con_pixeles = []
    archivos_problematicos = []

    # Itera sobre cada archivo en la carpeta especificada
    for nombre_archivo in os.listdir(carpeta_tiffs):
        # Solo procesa archivos TIFF
        if nombre_archivo.endswith('.tif') or nombre_archivo.endswith('.tiff'):
            ruta_archivo = os.path.join(carpeta_tiffs, nombre_archivo)  # Construye la ruta completa del archivo
            try:
                # Abre el archivo TIFF y recorta la imagen usando la geometría del shapefile
                with rasterio.open(ruta_archivo) as src:
                    imagen_recortada, transform = mask(src, geometria, crop=True, nodata=0)

                    # Verifica si hay píxeles distintos de 0 en la imagen recortada
                    if np.any(imagen_recortada != 0):
                        tiffs_con_pixeles.append(nombre_archivo)  # Añade el archivo a la lista de TIFFs válidos
            except rasterio.errors.RasterioIOError as e:
                # Maneja errores específicos de Rasterio al abrir el archivo
                print(f"Error al abrir {ruta_archivo}: {e}")
                archivos_problematicos.append(nombre_archivo)  # Añade el archivo a la lista de problemáticos
            except Exception as e:
                # Maneja cualquier otro tipo de error
                print(f"Error procesando {ruta_archivo}: {e}")
                archivos_problematicos.append(nombre_archivo)  # Añade el archivo a la lista de problemáticos

    return tiffs_con_pixeles, archivos_problematicos

def limpiar_nombres_tiffs(lista_tiffs):
    species_names = []  # Lista para almacenar los nombres limpios de las especies
    
    for nombre_archivo in lista_tiffs:
        # Limpiar el nombre del archivo eliminando ciertas partes y caracteres no deseados
        nombre_limpio = nombre_archivo.replace('_10_MAXENT.tif', '').replace('_veg.tif', '').replace('_pub.tif', '').replace('_con.tif', '').replace('_exp.tif', '').replace('.tif', '').replace('_pub1', ' ').replace('_', ' ')
        species_names.append(nombre_limpio)  # Añadir el nombre limpio a la lista
    
    return species_names  # Retorna la lista de nombres de especies limpiados

def procesar_varias_carpetas(carpetas_tiffs, archivo_shapefile):
    lista_especies = []  # Lista para almacenar todas las especies encontradas
    archivos_problematicos_totales = []  # Lista para almacenar todos los archivos problemáticos

    for carpeta_tiffs in carpetas_tiffs:
        # Llama a la función para procesar cada carpeta de TIFFs
        tiffs_validos, archivos_problematicos = recortar_y_filtrar_tiffs(carpeta_tiffs, archivo_shapefile)
        # Limpia los nombres de los archivos TIFF válidos
        species_names = limpiar_nombres_tiffs(tiffs_validos)
        lista_especies.extend(species_names)  # Añade los nombres limpios a la lista de especies
        archivos_problematicos_totales.extend(archivos_problematicos)  # Añade los archivos problemáticos a la lista total

    lista_especies = list(set(lista_especies))  # Elimina duplicados de la lista de especies
    return lista_especies, archivos_problematicos_totales

# Lista de carpetas que contienen los archivos TIFF
carpetas_tiffs = [] #Instertar rutas de las carpetas con los archivos .tif

# Ruta al archivo shapefile
archivo_shapefile = #Instertar ruta con archivo shape del polígono de interes

# Función para reproyectar el shapefile si su CRS es diferente al CRS de los modelos (EPSG:4326)
def reproyectar_shapefile(archivo_shapefile, crs_destino):
    try:
        with fiona.open(archivo_shapefile, 'r') as source:
            nuevas_geometrias = []  # Lista para almacenar las geometrías reproyectadas

            # Definir el CRS de origen y destino
            crs_origen = source.crs
            crs_destino_proj = CRS(crs_destino)
            crs_origen_proj = CRS(crs_origen)

            # Transformar las geometrías al nuevo CRS
            for feature in source:
                geometria_origen = feature["geometry"]
                geometria_destino = transform_geom(crs_origen_proj, crs_destino_proj, geometria_origen)
                nuevas_geometrias.append(geometria_destino)

        return nuevas_geometrias  # Devuelve la lista de geometrías reproyectadas
    except Exception as e:
        print(f"Error al procesar el CRS: {e}")
        return None


# Procesa todas las carpetas de TIFFs y obtiene la lista de especies y archivos problemáticos
lista_especies, archivos_problematicos = procesar_varias_carpetas(carpetas_tiffs, archivo_shapefile)

print(f"Nombres de especies sin duplicados: {lista_especies}")

if archivos_problematicos:
    print(f"Hubo {len(archivos_problematicos)} archivos problemáticos que no se pudieron procesar:")
    print(archivos_problematicos)

# Guarda la lista de especies sin duplicados en un archivo CSV
df_resultado = pd.DataFrame({'Especies': lista_especies})
df_resultado.to_csv("especies_final.csv", index=False)
print("Lista de especies guardada en 'especies_final.csv'")
