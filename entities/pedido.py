"""Entidad Pedido de Madriguera Market (contenido apto para todo publico UwU)."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from entities.excepciones import ErrorValidacion


@dataclass
class Pedido:
    id_usuario: int
    carrito: dict
    estado: str
    id: Optional[int] = None


    def __post_init__(self):
        if not self.estado:
            raise ErrorValidacion("El estado es obligatorio")
        if self.carrito is None:
            raise ErrorValidacion("El carrito no puede estar vacío OnO")
        if self.id_usuario is not None and self.id_usuario <= 0:
            raise ErrorValidacion("El ID de usuario debe ser un entero positivo OnO")
        if len(self.estado) > 15:
            raise ErrorValidacion("El estado no puede superar 15 caracteres")
    def editar_datos(self, carrito: Optional[dict], estado: Optional[str]) -> None:
        if not carrito:
            carrito = self.carrito
        if not estado:
            estado = self.estado

        self.carrito = carrito
        self.estado = estado

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "carrito": self.carrito,
            "estado": self.estado,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Pedido":
        return cls(
            id=datos.get("id"),
            id_usuario=datos.get("id_usuario"),
            carrito=datos.get("carrito"),
            estado=datos.get("estado"),
        )
