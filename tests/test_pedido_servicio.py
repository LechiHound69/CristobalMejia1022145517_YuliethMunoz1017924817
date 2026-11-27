"""Pruebas unitarias del CRUD de Pedido (casos exitosos y de error por operacion)."""

import os
import tempfile
import unittest

from entities.excepciones import (
    ErrorValidacion,
    PedidoNoEncontrado,
    ProductoAgotado,
)
from repositories.pedido_repositorio import PedidoRepositorio
from services.pedido_servicio import PedidoService


class PruebasPedidoServicio(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = os.path.join(carpeta.name, "data", "pedido_data.json")
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        self.servicio = PedidoService(PedidoRepositorio(self.ruta))
        self.servicio._repo.validar_inventario = lambda carrito: False
    def _crear_pedido(self, **extra):
        datos = {
            "id_usuario": 1,
            "carrito": {"1": 2},
            "estado": "Activo",
        }
        datos.update(extra)
        return self.servicio.crear(**datos)

    # CREAR
    def test_crear_exitoso_asigna_id(self):
        pedido = self._crear_pedido()
        self.assertIsNotNone(pedido.id)
        self.assertEqual(pedido.id_usuario, 1)
        self.assertEqual(pedido.estado, "Activo")

    def test_crear_con_id_usuario_invalido_falla(self):
        with self.assertRaises(ErrorValidacion):
            self._crear_pedido(id_usuario=0)

    def test_crear_con_estado_vacio_falla(self):
        with self.assertRaises(ErrorValidacion):
            self._crear_pedido(estado="")

    def test_crear_con_producto_agotado_falla(self):
        self.servicio._repo.validar_inventario = lambda carrito: True
        with self.assertRaises(ProductoAgotado):
            self._crear_pedido(carrito={"999": 99999})

    def test_obtener_exitoso(self):
        creado = self._crear_pedido()
        obtenido = self.servicio.obtener(creado.id)
        self.assertEqual(obtenido.id_usuario, 1)

    def test_obtener_inexistente_falla(self):
        with self.assertRaises(PedidoNoEncontrado):
            self.servicio.obtener(999)

    def test_obtener_por_usuario_devuelve_sus_pedidos(self):
        self._crear_pedido(id_usuario=1)
        self._crear_pedido(id_usuario=1, carrito={"2": 1})
        self._crear_pedido(id_usuario=2)
        pedidos_usuario_1 = self.servicio.obtener_por_usuario(1)
        self.assertEqual(len(pedidos_usuario_1), 2)

    def test_listar_devuelve_todos(self):
        self._crear_pedido(id_usuario=1)
        self._crear_pedido(id_usuario=2)
        self.assertEqual(len(self.servicio.listar()), 2)

    def test_listar_vacio(self):
        self.assertEqual(self.servicio.listar(), [])

    # ACTUALIZAR (editar_datos)
    def test_editar_datos_exitoso(self):
        creado = self._crear_pedido()
        actualizado = self.servicio.editar_datos(
            creado.id, carrito={"1": 5}, estado="Enviado"
        )
        self.assertEqual(actualizado.estado, "Enviado")
        self.assertEqual(self.servicio.obtener(creado.id).carrito, {"1": 5})

    def test_editar_datos_inexistente_falla(self):
        with self.assertRaises(PedidoNoEncontrado):
            self.servicio.editar_datos(999, estado="Inactivo")

    def test_editar_datos_con_estado_invalido_falla_y_no_cambia_nada(self):
        creado = self._crear_pedido()
        with self.assertRaises(ErrorValidacion):
            self.servicio.editar_datos(creado.id, estado="")
        self.assertEqual(self.servicio.obtener(creado.id).estado, "Activo")

    def test_editar_campo_no_editable_falla(self):
        creado = self._crear_pedido()
        with self.assertRaises(ErrorValidacion):
            self.servicio.editar_datos(creado.id, id_usuario=99)

    # ELIMINAR
    def test_eliminar_exitoso(self):
        creado = self._crear_pedido()
        self.servicio.eliminar(creado.id)
        self.assertEqual(self.servicio.obtener(creado.id).estado, "Cancelado")

    def test_eliminar_inexistente_falla(self):
        with self.assertRaises(PedidoNoEncontrado):
            self.servicio.eliminar(999)

    # PERSISTENCIA EN JSON
    def test_los_datos_sobreviven_al_reabrir_el_archivo(self):
        creado = self._crear_pedido()
        otro_servicio = PedidoService(PedidoRepositorio(self.ruta))
        self.assertEqual(otro_servicio.obtener(creado.id).id_usuario, 1)

    def test_archivo_vacio_se_trata_como_sin_pedidos(self):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("")
        servicio = PedidoService(PedidoRepositorio(self.ruta))
        self.assertEqual(servicio.listar(), [])


if __name__ == "__main__":
    unittest.main()
