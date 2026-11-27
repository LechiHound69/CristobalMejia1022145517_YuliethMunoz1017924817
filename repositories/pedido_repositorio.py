"""Acceso a datos de Pedido, guardado en un archivo JSON."""

from dataclasses import replace

from entities.pedido import Pedido
from repositories.base import Repositorio
from repositories.producto_repositorio import ProductoRepositorio

class PedidoRepositorio(Repositorio):
    def crear(self, pedido: Pedido) -> Pedido:
        nuevo_id = max((int(clave) for clave in self._buffer), default=0) + 1
        nuevo = replace(pedido, id=nuevo_id)
        self._buffer[str(nuevo_id)] = nuevo.to_dict()
        self._guardar()
        return nuevo

    def obtener_por_id(self, id: int) -> Pedido:
        clave = str(id)
        if clave not in self._buffer:
            raise KeyError(f"No existe ningún registro con el ID {id}. >n<")

        return Pedido.from_dict(self._buffer[clave])
       
    def obtener_por_usuario(self, id_usuario: int) -> list[Pedido]:
        return [
            Pedido.from_dict(datos)
            for datos in self._buffer.values()
            if int(datos["id_usuario"]) == int(id_usuario)
        ]    

    def obtener_todos(self) -> list[Pedido]:
        return [Pedido(**datos) for datos in self._buffer.values()]

    def actualizar(self, entidad: Pedido) -> Pedido:
        clave = str(entidad.id)
        if clave not in self._buffer:
            raise KeyError(
                f"No se puede actualizar el pedido con ID {clave} porque no existe UnU"
            )
        self._buffer[clave] = entidad.to_dict()
        self._guardar()
        return entidad

    def eliminar(self, id: int) -> bool:
        clave = str(id)
        if clave not in self._buffer:
            return False
        reg = self._buffer[clave]
        reg["estado"] = "Cancelado"
        self._buffer[clave] = reg
        self._guardar()
        return True

    def validar_inventario(self, carrito: dict) -> bool:
        producto_repo = ProductoRepositorio("./data/product_data.json")
        producto_buffer = producto_repo.get_buffer()
        for id_producto, cantidad in carrito.items():
            producto = producto_buffer.get(str(id_producto))
            if producto is None or int(producto["cantidad"]) < int(cantidad):
                return True
        return False   
