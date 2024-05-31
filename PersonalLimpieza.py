class PersonalLimpieza:
    def __init__(self, id:int) -> None:
        self.id = id
        self.estado = "Esperando Limpiar"
    
    def limpiar(self):
        self.estado = "Limpiando"