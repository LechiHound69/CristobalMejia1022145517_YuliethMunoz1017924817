import unittest

from entities.categoria import Categoria


class PruebasCategoriaEntidad(unittest.TestCase):
    def test_categoria_tiene_cuatro_valores(self):
        self.assertEqual(len(Categoria), 4)

    def test_valores_de_las_categorias(self):
        self.assertEqual(Categoria.ACCESORIOS.value, "Accesorios")
        self.assertEqual(Categoria.PELUCHES.value, "Peluches")
        self.assertEqual(Categoria.STICKERS_Y_PINES.value, "Stickers y pines")
        self.assertEqual(
            Categoria.ARTE_Y_COLECCIONABLES.value, "Arte y coleccionables"
        )

    def test_se_puede_crear_categoria_desde_su_valor(self):
        self.assertEqual(Categoria("Peluches"), Categoria.PELUCHES)

    def test_categoria_se_comporta_como_texto(self):
        self.assertEqual(Categoria.ACCESORIOS, "Accesorios")

    def test_valor_invalido_lanza_error(self):
        with self.assertRaises(ValueError):
            Categoria("Electrodomésticos")


if __name__ == "__main__":
    unittest.main()