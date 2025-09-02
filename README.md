# Numero de Especies Potenciales según BioModelos

Permite identificar qué **especies** (modeladas como archivos **TIFF**) están presentes en un área de interés definido por un **shapefile/GeoJSON**.  
Opcionalmente, los resultados pueden cruzarse con una base de datos externa en CSV/TSV.

---

## 📂 Estructura del Proyecto

```
Numero-de-especies-BioModelos/
│
├── src/numero_biomodelos/                 # Código fuente
│   ├── __init__.py
│   └── numero_especies.py
│
├── tests/                                 # Pruebas unitarias (pytest)
│   └── test_errors.py
│
├── examples/                              # Ejemplos de uso
│   ├── run_example.py
│   ├── example.ipynb
│   ├── shapefile_ejemplo
│   └── rasters_ejemplo
│                               
│
├── .github/workflows/ci.yml               # CI/CD (pytest en cada push/PR)
├── README.md
├── requirements.txt
├── environment.yml
├── LICENSE (MIT)
├── CITATION.cff
└── .gitignore
```

---

## ⚙️ Instalación

### Opción 1: con **pip**
```bash
pip install -r requirements.txt
```

### Opción 2: con **conda/mamba**
```bash
mamba env create -f environment.yml
mamba activate biomodelos
```

---

## ▶️ Ejemplo de uso básico

```python
from numero_biomodelos.numero_especies import (
    especies_en_area,
    verificar_y_transformar_crs_shapefile,
)

# Directorios con archivos .tif
directorios = ["data/rasters/"]

# Shapefile del área de interés
shapefile = "data/aoi/area_estudio.shp"

# Verificar y transformar AOI si es necesario
shapefile = verificar_y_transformar_crs_shapefile(shapefile)

# Identificar especies presentes
num_especies, lista_especies = especies_en_area(directorios, shapefile)

print(f"Número de especies: {num_especies}")
print("Especies presentes:", lista_especies)
```

---

## 📘 Ejemplo reproducible

Este repositorio incluye datos de **demo sintéticos** en `examples/`:

- Shapefile: `examples/shape_ejemplo/shape_ejemplo.shp`
- Rasters: `examples/rasters/Procyon_lotor_veg.tif`, `examples/rasters/Panthera_onca_veg.tif`, `examples/rasters/Nasua_nasua_veg.tif`

Ejecutar el ejemplo:

```bash
python examples/run_example.py
```

Salida esperada:

```
Número de especies presentes en el área: 2
Especies presentes: ['Nasua nasua', 'Panthera onca']
```

También puedes abrir `examples/example.ipynb` en Jupyter Notebook.

---

## 📑 Data inputs & provenance

El script trabaja con:

- **Shapefile (área de interés)**  
  - Formatos: Shapefile, GeoJSON, GPKG.  
  - Requiere **CRS válido**. Si no está en EPSG:4326, se transforma automáticamente.  

- **Rasters de especies**  
  - Formato: GeoTIFF.  
  - CRS esperado: EPSG:4326 (otros CRS se reproyectan en memoria).  
  - Valor `1` = presencia, `0` = ausencia.  
  - `nodata` se respeta al aplicar la máscara.  

- **Base de datos externa (opcional)**  
  - Formato: CSV o TSV.  
  - Debe contener una columna con nombres de especies (`especie` o `nombre_cientifico`).  

> ⚠️ Si usas datos de **BioModelos**, respeta sus términos de uso y cita adecuadamente.

---

## ❗ Errores comunes

| Código | Excepción             | ¿Cuándo ocurre?                                        | ¿Cómo solucionarlo? |
|:-----:|------------------------|--------------------------------------------------------|---------------------|
| E001  | `NoTiffsFoundError`    | No hay `.tif` en los directorios                       | Verifica rutas, permisos y extensiones |
| E002  | `InvalidAOIError`      | El AOI está vacío o no se pudo leer                    | Revisa geometrías y formato |
| E003  | `InvalidCRSError`      | El AOI o raster no tiene CRS válido (`.prj` ausente)   | Asigna un CRS válido (p.ej. EPSG:4326) |
| E9xx  | `ValueError` genérico  | Otros errores en reproyección o lectura                | Revisa el mensaje y la integridad de los datos |

---

## 🧪 Tests

Este repo usa **pytest** para pruebas unitarias.  
Ejecuta:

```bash
pytest -q
```

Los tests básicos verifican:
- Error si no hay `.tif` en el directorio.
- Error si el shapefile no tiene CRS.

---

## 📜 Licencia

Este proyecto está licenciado bajo **MIT License**.  
Consulta (LICENSE) para más información.

---

## 📖 Citación

Si usas este software en tu investigación, por favor cítalo así:

```bibtex
@software{numero_biomodelos,
  author       = {Garcia, Laura},
  title        = {Numero de Especies BioModelos},
  year         = {2025},
  publisher    = {Zenodo},
  version      = {0.1.0},
  doi          = {https://doi.org/10.5281/zenodo.17038514},
  url          = {https://github.com/Laur8629/Numero-de-especies-BioModelos}
}
```


