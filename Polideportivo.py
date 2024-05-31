class Polideportivo:
    def __init__(self) -> None:
        self.nombre = "Polideportivo General Paz"
        self.estado = "Cancha Libre"
        self.colaFyH = 0
        self.colaB = 0

    def ocupar(self, basquet=False):
        self.estado = "Cancha Ocupada"
        if basquet:
            self.colaB -= 1
        else:
            self.colaFyH -= 1