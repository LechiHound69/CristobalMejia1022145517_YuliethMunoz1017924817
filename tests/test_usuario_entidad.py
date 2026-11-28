"""Pruebas de las validaciones de la entidad Usuario."""

import unittest

from entities.excepciones import ErrorValidacion
from entities.usuario import Usuario


def _datos(**extra):
    datos = {
        "nombre": "Lechi Hound",
        "email": "lechi@madriguera.com",
        "documento": "1000123456",
        "telefono": "3001234567",
        "direccion": "Calle Falsa 123",
        "estado": "Activo",
    }
    datos.update(extra)
    return datos


class PruebasUsuarioEntidad(unittest.TestCase):
    def test_usuario_valido(self):
        usuario = Usuario(**_datos())
        self.assertEqual(usuario.nombre, "Lechi Hound")

    def test_nombre_con_espacios_se_limpia(self):
        usuario = Usuario(**_datos(nombre="  Lechi  ", direccion="  Calle 10  "))
        self.assertEqual(usuario.nombre, "Lechi")
        self.assertEqual(usuario.direccion, "Calle 10")

    def test_nombre_vacio_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(nombre="   "))

    def test_email_vacio_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(email=""))

    def test_documento_vacio_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(documento=""))

    def test_direccion_vacia_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(direccion="   "))

    def test_nombre_muy_largo_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(nombre="a" * 101))

    def test_documento_muy_largo_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(documento="1" * 17))

    def test_telefono_muy_largo_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(telefono="3" * 21))

    def test_direccion_muy_larga_falla(self):
        with self.assertRaises(ErrorValidacion):
            Usuario(**_datos(direccion="c" * 101))

    def test_to_dict_y_from_dict(self):
        original = Usuario(**_datos())
        diccionario = original.to_dict()
        reconstruido = Usuario.from_dict(diccionario)
        self.assertEqual(original, reconstruido)


if __name__ == "__main__":
    unittest.main()
