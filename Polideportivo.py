# Polideportivo.py
class Polideportivo:
    def __init__(self):
        self.nombre = "Polideportivo General Paz"
        self.estado = "Cancha Libre"
        self.colaFyH = 0
        self.colaB = 0
        self.cola = []

    def agregar_equipo(self, tipo):
        self.estado = "Cancha Ocupada"

    def liberar(self):
        self.estado = "Cancha Libre"

    def finalizar_limpieza(self):
        self.estado = "Cancha Libre"
