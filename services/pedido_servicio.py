"""Logica de negocio del CRUD de Pedido."""

from entities.excepciones import ErrorValidacion, PedidoNoEncontrado, ProductoAgotado
from entities.pedido import Pedido

CAMPOS_EDITABLES = {
    "carrito",
    "estado",
}


class PedidoService:

    def __init__(self, repositorio):
        self._repo = repositorio

    def crear(self, id_usuario: int, carrito: dict, estado="Activo"):
        pedido = Pedido(id_usuario=id_usuario, carrito=carrito, estado=estado)

        if self._repo.validar_inventario(carrito):
            raise ProductoAgotado(
                "Uno de los productos elegidos no tiene suficientes existencias UnU"
            )

        return self._repo.crear(pedido)

    def obtener(self, id: int) -> Pedido:
        try:
            return self._repo.obtener_por_id(id)
        except KeyError:
            raise PedidoNoEncontrado(f"No existe el pedido con el ID {id} OnO")

    def obtener_por_usuario(self, id_usuario: int) -> list[Pedido]:
        return self._repo.obtener_por_usuario(id_usuario)

    def listar(self) -> list[Pedido]:
        return self._repo.obtener_todos()

    def editar_datos(self, id: int, /, **cambios) -> Pedido:
        actual = self.obtener(id)

        invalidos = set(cambios) - CAMPOS_EDITABLES
        if invalidos:
            raise ErrorValidacion(
                f"Campos no editables TwT: {', '.join(sorted(invalidos))}"
            )
        if "carrito" in cambios and self._repo.validar_inventario(cambios["carrito"]):
            raise ProductoAgotado(
                "Uno de los productos elegidos no tiene suficientes existencias UnU"
            )

        datos = {**actual.to_dict(), **cambios}
        actualizado = Pedido.from_dict(datos)
        return self._repo.actualizar(actualizado)

    def eliminar(self, id: int) -> None:
        if not self._repo.eliminar(id):
            raise PedidoNoEncontrado(f"No existe pedido con ese ID {id} UnU")