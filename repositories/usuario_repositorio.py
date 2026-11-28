"""Acceso a datos de Usuario, guardado en un archivo JSON."""

from dataclasses import replace
from typing import Optional

from entities.usuario import Usuario
from repositories.base import Repositorio


class UsuarioRepositorio(Repositorio):
    def crear(self, usuario: Usuario) -> Usuario:
        nuevo_id = max((int(clave) for clave in self._buffer), default=0) + 1
        nuevo = replace(usuario, id=nuevo_id)
        self._buffer[str(nuevo_id)] = nuevo.to_dict()
        self._guardar()
        return nuevo

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        clave = str(id)
        if clave not in self._buffer:
            raise KeyError(f"No existe ningún registro con el ID {id}. >n<")

        return Usuario.from_dict(self._buffer[clave])

    def obtener_todos(self) -> list[Usuario]:
        return [Usuario.from_dict(datos) for datos in self._buffer.values()]

    def actualizar(self, usuario: Usuario) -> Usuario:
        clave = str(usuario.id)
        if clave not in self._buffer:
            raise KeyError(
                f"No se puede actualizar el usuario con ID {clave} porque no existe UnU"
            )
        self._buffer[clave] = usuario.to_dict()
        self._guardar()
        return usuario

    def eliminar(self, id: int) -> bool:
        clave = str(id)
        if clave not in self._buffer:
            return False
        reg = self._buffer[clave]
        reg["estado"] = "Inactivo"
        self._buffer[clave] = reg
        self._guardar()
        return True

    def existe_email(self, email: str, excluir_id: Optional[int] = None) -> bool:
        email = email.strip().lower()
        return any(
            datos["email"].lower() == email and datos["id"] != excluir_id
            for datos in self._buffer.values()
        )

    def existe_documento(
        self, documento: str, excluir_id: Optional[int] = None
    ) -> bool:
        documento = documento.strip().lower()
        return any(
            datos["documento"].lower() == documento and datos["id"] != excluir_id
            for datos in self._buffer.values()
        )
