import unittest
from logica_negocio.coordenada import Coordenada
from logica_negocio.calculadora_geografica import CalculadoraGeografica

class TestCalculadoraGeografica(unittest.TestCase):
    def test_convertir_a_decimal(self):
        coord = Coordenada(10, 30, 0)
        self.assertEqual(coord.decimal, 10.5)

    def test_calcular_distancia(self):
        coord1 = Coordenada(0, 0, 0)
        coord2 = Coordenada(0, 1, 0)
        calculadora = CalculadoraGeografica()
        distancia = calculadora.calcular_distancia(coord1, coord2)
        self.assertAlmostEqual(distancia, 111.19, places=2)

    def test_calcular_rumbo(self):
        coord1 = Coordenada(0, 0, 0, 'N')
        coord2 = Coordenada(0, 1, 0, 'N')
        coord1.lon_decimal = 0.0
        coord2.lon_decimal = 1.0
        calculadora = CalculadoraGeografica()
        rumbo = calculadora.calcular_rumbo(coord1, coord2)
        self.assertAlmostEqual(rumbo, 90.0, places=1)

    def test_calcular_azimut(self):
        coord1 = Coordenada(0, 0, 0, 'N')
        coord2 = Coordenada(0, 1, 0, 'N')
        coord1.lon_decimal = 0.0
        coord2.lon_decimal = 1.0
        calculadora = CalculadoraGeografica()
        azimut = calculadora.calcular_azimut(coord1, coord2)
        self.assertAlmostEqual(azimut, 90.0, places=1)

if __name__ == '__main__':
    unittest.main()
