from logica_negocio.coordenada import Coordenada
class PuntoGeografico:
    def __init__(self, latitud: Coordenada, longitud: Coordenada):
        self.latitud = latitud
        self.longitud = longitud
