# tests/test_errors.py

import os
import json
import geopandas as gpd
from shapely.geometry import Polygon
import pytest

# Ajusta el import a la ruta real de tu módulo/script
# Si lo tienes como script plano, puedes convertirlo en paquete o usar sys.path.append
from Riqueza_especies import (
    especies_en_area,
    verificar_y_transformar_crs_shapefile,
    NoTiffsFoundError,
    InvalidCRSError,
)

def crear_aoi_geojson_sin_crs(ruta_geojson):
    """Crea un GeoJSON de AOI sin CRS (sin 'crs' ni .prj)."""
    poly = Polygon([(0,0), (1,0), (1,1), (0,1)])
    gdf = gpd.GeoDataFrame({"id":[1]}, geometry=[poly], crs=None)  # crs=None
    # Guardamos como GeoJSON “a mano” para evitar que geopandas añada CRS por defecto
    features = [{
        "type": "Feature",
        "properties": {"id": 1},
        "geometry": gdf.geometry.iloc[0].__geo_interface__,
    }]
    with open(ruta_geojson, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f)
    return ruta_geojson

def crear_aoi_shapefile_con_crs(ruta_dir):
    """Crea un shapefile con CRS válido (EPSG:4326)."""
    poly = Polygon([(0,0), (1,0), (1,1), (0,1)])
    gdf = gpd.GeoDataFrame({"id":[1]}, geometry=[poly], crs="EPSG:4326")
    aoi_path = os.path.join(ruta_dir, "aoi_ok.shp")
    gdf.to_file(aoi_path)
    return aoi_path

def test_no_tiffs(tmp_path):
    """Debe fallar con NoTiffsFoundError cuando no hay .tif en directorios."""
    # Directorio vacío (sin .tif)
    dir_vacio = tmp_path / "rasters"
    dir_vacio.mkdir()

    # AOI válido con CRS para que falle solo por ausencia de tiffs
    aoi_ok = crear_aoi_shapefile_con_crs(str(tmp_path))

    with pytest.raises(NoTiffsFoundError):
        especies_en_area([str(dir_vacio)], aoi_ok)

def test_aoi_sin_crs(tmp_path):
    """Debe fallar con InvalidCRSError cuando el AOI no tiene CRS."""
    aoi_sin_crs = tmp_path / "aoi_sin_crs.geojson"
    crear_aoi_geojson_sin_crs(str(aoi_sin_crs))

    with pytest.raises(InvalidCRSError):
        verificar_y_transformar_crs_shapefile(str(aoi_sin_crs))
