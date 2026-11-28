"""Pruebas unitarias del CRUD de Usuario (casos exitosos y de error por operacion)."""

import os
import tempfile
import unittest

from entities.excepciones import (
    ErrorValidacion,
    UsuarioDuplicado,
    UsuarioNoEncontrado,
)
from repositories.usuario_repositorio import UsuarioRepositorio
from services.usuario_servicio import UsuarioServicio


class PruebasUsuarioServicio(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = os.path.join(carpeta.name, "data", "user_data.json")
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        self.servicio = UsuarioServicio(UsuarioRepositorio(self.ruta))

    def _crear_usuario(self, **extra):
        datos = {
            "nombre": "Lechi",
            "email": "lechi@madriguera.com",
            "documento": "1000123456",
            "telefono": "3001234567",
            "direccion": "Calle Falsa 123",
            "estado": "Activo",
        }
        datos.update(extra)
        return self.servicio.crear(**datos)

    # CREAR
    def test_crear_exitoso_asigna_id(self):
        usuario = self._crear_usuario()
        self.assertEqual(usuario.id, 1)
        self.assertEqual(usuario.nombre, "Lechi")

    def test_crear_con_nombre_vacio_falla(self):
        with self.assertRaises(ErrorValidacion):
            self._crear_usuario(nombre="   ")

    def test_crear_con_email_repetido_falla(self):
        self._crear_usuario()
        with self.assertRaises(UsuarioDuplicado):
            self._crear_usuario(email="otro@madriguera.com")

    # LEER
    def test_obtener_exitoso(self):
        creado = self._crear_usuario()
        self.assertEqual(self.servicio.obtener(creado.id).nombre, "Lechi")

    def test_obtener_inexistente_falla(self):
        with self.assertRaises(UsuarioNoEncontrado):
            self.servicio.obtener(999)

    def test_listar_devuelve_todos(self):
        self._crear_usuario()
        self._crear_usuario(
            nombre="Haruna",
            email="haruna@madriguera.com",
            documento="2000654321",
        )
        self.assertEqual(len(self.servicio.listar()), 2)

    def test_listar_vacio(self):
        self.assertEqual(self.servicio.listar(), [])

    # ACTUALIZAR (editar_datos)
    def test_editar_datos_exitoso(self):
        creado = self._crear_usuario()
        actualizado = self.servicio.editar_datos(
            creado.id, nombre="Lechi Hound", telefono="3110000000"
        )
        self.assertEqual(actualizado.nombre, "Lechi Hound")
        self.assertEqual(self.servicio.obtener(creado.id).telefono, "3110000000")

    def test_editar_datos_inexistente_falla(self):
        with self.assertRaises(UsuarioNoEncontrado):
            self.servicio.editar_datos(999, nombre="Fantasma")

    def test_editar_datos_con_dato_invalido_falla_y_no_cambia_nada(self):
        creado = self._crear_usuario()
        with self.assertRaises(ErrorValidacion):
            self.servicio.editar_datos(creado.id, nombre="   ")
        self.assertEqual(self.servicio.obtener(creado.id).nombre, "Lechi")

    def test_editar_campo_no_editable_falla(self):
        creado = self._crear_usuario()
        with self.assertRaises(ErrorValidacion):
            self.servicio.editar_datos(creado.id, id=50)

    def test_editar_a_email_existente_falla(self):
        self._crear_usuario()
        otro = self._crear_usuario(
            nombre="Haruna",
            email="haruna@madriguera.com",
            documento="2000654321",
        )
        with self.assertRaises(UsuarioDuplicado):
            self.servicio.editar_datos(otro.id, email="lechi@madriguera.com")

    # ELIMINAR
    def test_eliminar_exitoso(self):
        creado = self._crear_usuario()
        self.servicio.eliminar(creado.id)
        self.assertEqual(self.servicio.obtener(creado.id).estado, "Inactivo")
        

    def test_eliminar_inexistente_falla(self):
        with self.assertRaises(UsuarioNoEncontrado):
            self.servicio.eliminar(999)

    # PERSISTENCIA EN JSON
    def test_los_datos_sobreviven_al_reabrir_el_archivo(self):
        creado = self._crear_usuario()
        otro_servicio = UsuarioServicio(UsuarioRepositorio(self.ruta))
        self.assertEqual(otro_servicio.obtener(creado.id).nombre, "Lechi")

    def test_archivo_vacio_se_trata_como_sin_usuarios(self):
        with open(self.ruta, "w", encoding="utf-8") as archivo:
            archivo.write("")
        servicio = UsuarioServicio(UsuarioRepositorio(self.ruta))
        self.assertEqual(servicio.listar(), [])


if __name__ == "__main__":
    unittest.main()
