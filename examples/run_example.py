"""
Ejemplo mínimo de uso del paquete numero_biomodelos.
Usa datos sintéticos o de ejemplo que estén en la carpeta `examples/`.
"""

import os
from numero_biomodelos.numero_especies import (
    especies_en_area,
    verificar_y_transformar_crs_shapefile,
)

# Configuración de rutas de ejemplo
directorios = ["examples/rasters_ejemplo/"]
shapefile = "examples/shape_ejemplo/shape_ejemplo.shp"

# Verificar y transformar el AOI si es necesario
shapefile = verificar_y_transformar_crs_shapefile(shapefile)

# Evaluar especies presentes en el área de estudio
resultado = especies_en_area(directorios, shapefile)

print("Resultado del ejemplo:", resultado)
