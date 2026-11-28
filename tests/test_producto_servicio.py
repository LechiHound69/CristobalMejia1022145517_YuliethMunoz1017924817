"""Pruebas unitarias del CRUD de Producto (un caso exitoso y uno de error por operacion)."""

import os
import tempfile
import unittest

from entities.categoria import Categoria
from entities.excepciones import (
    ErrorValidacion,
    ProductoDuplicado,
    ProductoNoEncontrado,
)
from repositories.producto_repositorio import ProductoRepositorio
from services.producto_servicio import ProductoServicio


class PruebasProductoServicio(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = os.path.join(carpeta.name, "data", "product_data.json")
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        self.servicio = ProductoServicio(ProductoRepositorio(self.ruta))

    def _crear_orejas(self, **extra):
        datos = {
            "nombre": "Orejas de zorro",
            "descripcion": "Diadema suave",
            "precio": 35000,
            "cantidad": 10,
            "categoria": Categoria.ACCESORIOS,
        }
        datos.update(extra)
        return self.servicio.crear(**datos)

    # CREAR
    def test_crear_exitoso_asigna_id(self):
        producto = self._crear_orejas()
        self.assertEqual(producto.id, 1)
        self.assertEqual(producto.nombre, "Orejas de zorro")

    def test_crear_con_precio_negativo_falla(self):
        with self.assertRaises(ErrorValidacion):
            self._crear_orejas(precio=-5)

    def test_crear_con_nombre_repetido_falla(self):
        self._crear_orejas()
        with self.assertRaises(ProductoDuplicado):
            self._crear_orejas(nombre="orejas de ZORRO")

    # LEER
    def test_obtener_exitoso(self):
        creado = self._crear_orejas()
        self.assertEqual(self.servicio.obtener(creado.id).nombre, "Orejas de zorro")

    def test_obtener_inexistente_falla(self):
        with self.assertRaises(ProductoNoEncontrado):
            self.servicio.obtener(999)

    def test_listar_devuelve_todos(self):
        self._crear_orejas()
        self._crear_orejas(nombre="Cola de lobo")
        self.assertEqual(len(self.servicio.listar()), 2)

    def test_listar_vacio(self):
        self.assertEqual(self.servicio.listar(), [])

    # ACTUALIZAR
    def test_actualizar_exitoso(self):
        creado = self._crear_orejas()
        actualizado = self.servicio.actualizar(creado.id, precio=40000, cantidad=3)
        self.assertEqual(actualizado.precio, 40000)
        self.assertEqual(self.servicio.obtener(creado.id).cantidad, 3)

    def test_actualizar_inexistente_falla(self):
        with self.assertRaises(ProductoNoEncontrado):
            self.servicio.actualizar(999, precio=100)

    def test_actualizar_con_dato_invalido_falla_y_no_cambia_nada(self):
        creado = self._crear_orejas()
        with self.assertRaises(ErrorValidacion):
            self.servicio.actualizar(creado.id, precio=0)
        self.assertEqual(self.servicio.obtener(creado.id).precio, 35000)

    def test_actualizar_campo_no_editable_falla(self):
        creado = self._crear_orejas()
        with self.assertRaises(ErrorValidacion):
            self.servicio.actualizar(creado.id, id=50)

    def test_actualizar_a_nombre_existente_falla(self):
        self._crear_orejas()
        otro = self._crear_orejas(nombre="Cola de lobo")
        with self.assertRaises(ProductoDuplicado):
            self.servicio.actualizar(otro.id, nombre="Orejas de zorro")

    #  ELIMINAR
    def test_eliminar_exitoso(self):
        creado = self._crear_orejas()
        self.servicio.eliminar(creado.id)
        with self.assertRaises(ProductoNoEncontrado):
            self.servicio.obtener(creado.id)

    def test_eliminar_inexistente_falla(self):
        with self.assertRaises(ProductoNoEncontrado):
            self.servicio.eliminar(999)

    # PERSISTENCIA EN JSON
    def test_los_datos_sobreviven_al_reabrir_el_archivo(self):
        creado = self._crear_orejas()
        otro_servicio = ProductoServicio(ProductoRepositorio(self.ruta))
        self.assertEqual(otro_servicio.obtener(creado.id).nombre, "Orejas de zorro")

    def test_archivo_vacio_se_trata_como_sin_productos(self):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("")
        servicio = ProductoServicio(ProductoRepositorio(self.ruta))
        self.assertEqual(servicio.listar(), [])

    # DESCONTAR STOCK -
    def test_descontar_stock_exitoso(self):
        creado = self._crear_orejas(cantidad=10)
        self.assertEqual(self.servicio.descontar_stock(creado.id, 4).cantidad, 6)

    def test_descontar_mas_de_lo_disponible_falla(self):
        creado = self._crear_orejas(cantidad=2)
        with self.assertRaises(ErrorValidacion):
            self.servicio.descontar_stock(creado.id, 5)


if __name__ == "__main__":
    unittest.main()
