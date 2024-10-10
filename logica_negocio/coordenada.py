class Coordenada:
    def __init__(self, grados, minutos, segundos, direccion):
        self.grados = grados
        self.minutos = minutos
        self.segundos = segundos
        self.direccion = direccion.upper()
        self.decimal = self.convertir_a_decimal()
    
    def convertir_a_decimal(self):
        decimal = abs(self.grados) + self.minutos / 60 + self.segundos / 3600
        if self.direccion in ['S', 'W']:
            decimal = -decimal
        return decimal
