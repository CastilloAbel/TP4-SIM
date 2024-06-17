class Temporal:
    def __init__(self, nombre, estado, hora_llegada):
        self.nombre = nombre
        self.estado = estado
        self.hora_llegada = hora_llegada

    def set_estado(self, estado):
        self.estado = estado

    def truncar(self, numero, decimales=3):
        if numero is not None:
            factor = 10 ** decimales
            return int(numero * factor) / factor
        else:
            return ""
    
    def __str__(self):
        nombre = ""
        if self.estado is True and self.nombre in ("Futbol", "Basquet", "Handball"):
            nombre = "Jugando"
        elif self.estado is True and self.nombre == "Personal Limpieza":
            nombre = "Limpiando"
        elif self.estado is False:
            nombre = "Esperando"
        return f"Nombre: {self.nombre}, Estado: {nombre}, Hora de llegada: {self.truncar(self.hora_llegada)}\n"
