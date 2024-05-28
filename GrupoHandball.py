class GrupoHandball:
    def __init__(self, id:int) -> None:
        self.id = id
        self.estado = "Esperando Jugar"

    def jugar(self):
        self.estado = "Jugando"