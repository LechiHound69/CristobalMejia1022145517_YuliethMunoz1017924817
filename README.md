# Madriguera Market

Catálogo de productos para fans del mundo furry, con gestión completa de inventario. Proyecto académico, contenido apto para todo público.

## Estructura del proyecto

```
entities/       Entidades del dominio (Producto, Usuario, Pedido, Categoria)
repositories/   Acceso y persistencia de datos en archivos JSON
services/       Lógica de negocio (CRUD de productos, usuarios y pedidos)
data/           Archivos JSON con los datos
tests/          Pruebas unitarias
.github/workflows/  Flujo de CI/CD con GitHub Actions
```

## Requisitos

- Python 3.12
- Dependencias del archivo `requirements.txt`

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar las pruebas

```bash
python -m unittest discover -v
```

Con reporte de cobertura:

```bash
pip install coverage
coverage run -m unittest discover
coverage report -m
```

## CI/CD

El flujo de `.github/workflows/ci-cd.yaml` se ejecuta con cada push o pull request:

1. **CI:** instala dependencias, revisa la sintaxis con Flake8, corre las pruebas con cobertura mínima del 80 % y sube el reporte como artefacto.
2. **QA** (rama `Qa`): empaqueta la aplicación en un `.zip`.
3. **PROD** (rama `Prod`): publica un Release automático con el `.zip`.

Flujo de ramas: `feature/*` → `Dev` → `Qa` → `Prod`.

## Nota

Este repositorio es un fork del proyecto de la entrega anterior, renombrado para la actividad de CI/CD de Aplicaciones y servicios web (ITM).
