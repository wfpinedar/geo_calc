import math
from logica_negocio.punto_geografico import PuntoGeografico


class CalculadoraGeografica:
    def calcular_distancia(self, punto1: PuntoGeografico, punto2: PuntoGeografico):
        R = 6371  # Radio de la Tierra en kilómetros

        lat1 = math.radians(punto1.latitud.decimal)
        lon1 = math.radians(punto1.longitud.decimal)
        lat2 = math.radians(punto2.latitud.decimal)
        lon2 = math.radians(punto2.longitud.decimal)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = math.sin(delta_lat / 2) ** 2 + \
            math.cos(lat1) * math.cos(lat2) * \
            math.sin(delta_lon / 2) ** 2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distancia = R * c
        return distancia
    

    def calcular_rumbo(self, punto1: PuntoGeografico, punto2: PuntoGeografico):
        # Convertir coordenadas a radianes
        lat1 = math.radians(punto1.latitud.decimal)
        lon1 = math.radians(punto1.longitud.decimal)
        lat2 = math.radians(punto2.latitud.decimal)
        lon2 = math.radians(punto2.longitud.decimal)

        # Calcular las diferencias
        delta_lon = lon2 - lon1
        delta_lat = lat2 - lat1

        # Calcular el ángulo inicial
        rumbo_rad = math.atan2(
            math.sin(delta_lon),
            math.cos(lat1) * math.tan(lat2) - math.sin(lat1) * math.cos(delta_lon)
        )

        # Convertir a grados
        rumbo_grados = math.degrees(rumbo_rad)

        # Normalizar el ángulo
        if rumbo_grados < 0:
            rumbo_grados += 360

        # Determinar el cuadrante y el rumbo en formato cuadrantal
        if rumbo_grados >= 0 and rumbo_grados < 90:
            cuadrante = "Norte - Este"
            angulo_cuadrantal = rumbo_grados
        elif rumbo_grados >= 90 and rumbo_grados < 180:
            cuadrante = "Sur - Este"
            angulo_cuadrantal = 180 - rumbo_grados
        elif rumbo_grados >= 180 and rumbo_grados < 270:
            cuadrante = "Sur - Oeste"
            angulo_cuadrantal = rumbo_grados - 180
        else:
            cuadrante = "Norte - Oeste"
            angulo_cuadrantal = 360 - rumbo_grados

        # Retornar el rumbo en formato cuadrantal
        rumbo = f"{cuadrante}, {angulo_cuadrantal:.2f}°"
        return rumbo
    
    def calcular_azimut(self, punto1: PuntoGeografico, punto2: PuntoGeografico):
        lat1 = math.radians(punto1.latitud.decimal)
        lon1 = math.radians(punto1.longitud.decimal)
        lat2 = math.radians(punto2.latitud.decimal)
        lon2 = math.radians(punto2.longitud.decimal)

        delta_lon = lon2 - lon1

        x = math.sin(delta_lon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - \
            math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

        azimut_rad = math.atan2(x, y)
        azimut_grados = (math.degrees(azimut_rad) + 360) % 360

        return azimut_grados


