"""Pruebas de las validaciones de la entidad Pedido."""

import unittest

from entities.excepciones import ErrorValidacion
from entities.pedido import Pedido


def _datos(**extra):
    datos = {
        "id": "PED-001",
        "id_usuario": 1,
        "carrito": {"prod_1": 2, "prod_2": 1},
        "estado": "PENDIENTE",
    }
    datos.update(extra)
    return datos


class PruebasPedidoEntidad(unittest.TestCase):
    def test_pedido_valido(self):
        pedido = Pedido(**_datos())
        self.assertEqual(pedido.id, "PED-001")
        self.assertEqual(pedido.estado, "PENDIENTE")

    def test_estado_vacio_falla(self):
        with self.assertRaises(ErrorValidacion):
            Pedido(**_datos(estado=""))

    def test_estado_muy_largo_falla(self):
        with self.assertRaises(ErrorValidacion):
            Pedido(**_datos(estado="A" * 16))
            
    def test_id_usuario_cero_o_negativo_falla(self):
        with self.assertRaises(ErrorValidacion):
            Pedido(**_datos(id_usuario=0))
        with self.assertRaises(ErrorValidacion):
            Pedido(**_datos(id_usuario=-3))

    def test_editar_datos_actualiza_valores(self):
        pedido = Pedido(**_datos())
        nuevo_carrito = {"prod_3": 5}
        pedido.editar_datos(carrito=nuevo_carrito, estado="ENVIADO")
        self.assertEqual(pedido.carrito, nuevo_carrito)
        self.assertEqual(pedido.estado, "ENVIADO")

    def test_editar_datos_con_nulos_conserva_actuales(self):
        pedido = Pedido(**_datos())
        carrito_original = pedido.carrito
        pedido.editar_datos(carrito=None, estado=None)
        self.assertEqual(pedido.carrito, carrito_original)
        self.assertEqual(pedido.estado, "PENDIENTE")

    def test_to_dict_y_from_dict(self):
        original = Pedido(**_datos())
        diccionario = original.to_dict()
        reconstruido = Pedido.from_dict(diccionario)
        self.assertEqual(original, reconstruido)


if __name__ == "__main__":
    unittest.main()
