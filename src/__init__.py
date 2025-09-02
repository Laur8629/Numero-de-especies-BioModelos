"""
Paquete numero_biomodelos
Herramientas para identificar especies presentes en un área a partir de rasters (BioModelos u otros).
Re-exporta las funciones y excepciones principales desde `numero_especies.py`.
"""

from .numero_especies import (
    listar_tiffs,
    leer_raster,
    reproyectar_raster,
    verificar_y_transformar_crs_shapefile,
    limpiar_nombres_tiffs,
    especies_en_area,
    cruzar_con_base_datos,
    # Excepciones
    NoTiffsFoundError,
    InvalidAOIError,
    InvalidCRSError,
)

__all__ = [
    "listar_tiffs",
    "leer_raster",
    "reproyectar_raster",
    "verificar_y_transformar_crs_shapefile",
    "limpiar_nombres_tiffs",
    "especies_en_area",
    "cruzar_con_base_datos",
    # Excepciones
    "NoTiffsFoundError",
    "InvalidAOIError",
    "InvalidCRSError",
]
