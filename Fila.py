from Temporal import Temporal
import random
import math
class Fila:
    def __init__(self, id, reloj=0.0, eventos=[], estado_cancha="Cancha Libre", colaB=[], colaFyH=[],tiempo_espera_futbol=0, tiempo_espera_basquetball=0, tiempo_espera_handball=0, tiempo_espera_ocupacion_limpieza=0, objetos=[]) -> None:
        self.id = id
        self.nombre_evento = ""
        self.reloj = reloj
        self.eventos = eventos
        self.estado_cancha = estado_cancha
        self.colaB = colaB
        self.colaFyH = colaFyH
        self.tiempo_espera_futbol = tiempo_espera_futbol
        self.tiempo_espera_basquetball = tiempo_espera_basquetball
        self.tiempo_espera_handball = tiempo_espera_handball
        self.tiempo_espera_ocupacion_limpieza = tiempo_espera_ocupacion_limpieza
        self.objetos = objetos
 
    

    def equipo_futbol(self, nombre, estado, hora_llegada):
        return Temporal(nombre, estado, hora_llegada)
    def equipo_basquet(self, nombre, estado, hora_llegada):
        return Temporal(nombre, estado, hora_llegada)
    def equipo_handball(self, nombre, estado, hora_llegada):
        return Temporal(nombre, estado, hora_llegada)
    def personal_limpieza(self, nombre, estado, hora_llegada):
        return Temporal(nombre, estado, hora_llegada)
    
    def distribucion_exponencial(self, rnd, media):
        return (-1 * media) * math.log(1 - rnd)
    def distribucion_uniforme(self, rnd, inf, sup):
        return inf + (sup - inf) * rnd
    
    def simular(self, datos):
        
        [tiempo_total, tiempo_demora_limpieza, media_llegada_futbol, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup, 
                 intervalo_llegada_handball_inf, intervalo_llegada_handball_sup, fin_ocupacion_futbol_inf, fin_ocupacion_futbol_sup,
                 fin_ocupacion_basquet_inf, fin_ocupacion_basquet_sup, fin_ocupacion_handball_inf, fin_ocupacion_handball_sup, cantidad_equipos_max] = datos

        if self.reloj == 0:
            self.nombre_evento = "Inicializacion"
            rnd_llegada_futbol = random.random()
            llegada_futbol = self.distribucion_exponencial(rnd_llegada_futbol, media_llegada_futbol)
            rnd_llegada_basquet = random.random()
            llegada_basquet = self.distribucion_uniforme(rnd_llegada_basquet, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup)
            rnd_llegada_handball = random.random()
            llegada_handball = self.distribucion_uniforme(rnd_llegada_handball, intervalo_llegada_handball_inf, intervalo_llegada_handball_sup)
            self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                            [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                            [rnd_llegada_handball, llegada_handball, self.reloj + llegada_handball],
                            [None, None, None], [None, None, None], [None, None, None], [None, None, None]]
            reloj = min((evento[2] for evento in self.eventos if evento[2] is not None), default=None)
            return [reloj, self.eventos, self.estado_cancha, [], [], self.tiempo_espera_futbol, self.tiempo_espera_basquetball, self.tiempo_espera_handball, self.tiempo_espera_ocupacion_limpieza, []]
        else:
            self.reloj = min((evento[2] for evento in self.eventos if evento[2] is not None), default=None)
            #self.reloj = min(self.eventos[0][2], self.eventos[1][2], self.eventos[2][2], self.eventos[3][2], self.eventos[4][2], self.eventos[5][2], self.eventos[6][2])

            if self.reloj == self.eventos[0][2]:
                rnd_llegada_futbol = random.random()
                llegada_futbol = self.distribucion_exponencial(rnd_llegada_futbol, media_llegada_futbol)
                self.nombre_evento = "Llegada Equipo de Futbol"
                if (len(self.colaFyH) + len(self.colaB) < cantidad_equipos_max):
                    if self.estado_cancha == "Cancha Libre":
                        self.estado_cancha = "Cancha ocupada"
                        self.objetos.append(self.equipo_futbol("Futbol",True, self.reloj))
                        rnd_ocupacion_futbol = random.random()
                        fin_ocupacion_futbol = self.distribucion_uniforme(rnd_ocupacion_futbol, fin_ocupacion_futbol_inf,fin_ocupacion_futbol_sup)
                        self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                                        self.eventos[1], 
                                        self.eventos[2],
                                        [rnd_ocupacion_futbol, fin_ocupacion_futbol, self.reloj + fin_ocupacion_futbol], 
                                        self.eventos[4], self.eventos[5], self.eventos[6]]
                    else:
                        equipo = self.equipo_futbol("Futbol", False, self.reloj)
                        self.colaFyH.append(equipo)
                        self.objetos.append(equipo)
                        self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                                        self.eventos[1], 
                                        self.eventos[2],
                                        self.eventos[3], 
                                        self.eventos[4], self.eventos[5], self.eventos[6]]
                else:
                    self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                                    self.eventos[1], 
                                    self.eventos[2],
                                    self.eventos[3], 
                                    self.eventos[4], self.eventos[5], self.eventos[6]]
            elif self.reloj == self.eventos[1][2]:
                rnd_llegada_basquet = random.random()
                llegada_basquet = self.distribucion_uniforme(rnd_llegada_basquet, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup)
                self.nombre_evento = "Llegada Equipo de BasquetBall"
                if (len(self.colaFyH) + len(self.colaB) < cantidad_equipos_max):
                    if self.estado_cancha == "Cancha Libre":
                        self.estado_cancha = "Cancha ocupada"
                        self.objetos.append(self.equipo_basquet("Basquet", True, self.reloj))
                        rnd_ocupacion_basquet = random.random()
                        fin_ocupacion_basquet  = self.distribucion_uniforme(rnd_ocupacion_basquet, fin_ocupacion_basquet_inf,fin_ocupacion_basquet_sup)
                        self.eventos = [self.eventos[0], 
                                        [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                                        self.eventos[2],
                                        self.eventos[3], 
                                        [rnd_ocupacion_basquet, fin_ocupacion_basquet, self.reloj + fin_ocupacion_basquet], 
                                        self.eventos[5], self.eventos[6]]
                    else:
                        equipo = self.equipo_basquet("Basquet", False, self.reloj)
                        self.colaB.append(equipo)
                        self.objetos.append(equipo)
                        self.eventos = [self.eventos[0], 
                                        [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                                        self.eventos[2],
                                        self.eventos[3], 
                                        self.eventos[4], 
                                        self.eventos[5], self.eventos[6]]
                else:
                    self.eventos = [self.eventos[0], 
                                    [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                                    self.eventos[2],
                                    self.eventos[3], 
                                    self.eventos[4], 
                                    self.eventos[5], self.eventos[6]]
            elif self.reloj == self.eventos[2][2]:
                rnd_llegada_handball = random.random()
                llegada_handball = self.distribucion_uniforme(rnd_llegada_handball, intervalo_llegada_handball_inf, intervalo_llegada_handball_sup)
                self.nombre_evento = "Llegada Equipo de Handball"
                if (len(self.colaFyH) + len(self.colaB) < cantidad_equipos_max):
                    if self.estado_cancha == "Cancha Libre":
                        self.estado_cancha = "Cancha ocupada"
                        self.objetos.append(self.equipo_handball("Handball", True, self.reloj))
                        rnd_ocupacion_handball = random.random()
                        fin_ocupacion_handball  = self.distribucion_uniforme(rnd_ocupacion_handball, fin_ocupacion_handball_inf,fin_ocupacion_handball_sup)
                        self.eventos = [self.eventos[0],
                                        self.eventos[1],
                                        [rnd_llegada_handball, llegada_handball, self.reloj + llegada_handball],
                                        self.eventos[3],
                                        self.eventos[4],
                                        [rnd_ocupacion_handball, fin_ocupacion_handball, self.reloj + fin_ocupacion_handball], 
                                        self.eventos[6]]
                    else:
                        equipo = self.equipo_handball("Handball", False, self.reloj)
                        self.colaFyH.append(equipo)
                        objetos = self.objetos
                        objetos.append(equipo)
                        self.objetos = objetos
                        self.eventos = [self.eventos[0],
                                        self.eventos[1],
                                        [rnd_llegada_handball, llegada_handball, self.reloj + llegada_handball],
                                        self.eventos[3],
                                        self.eventos[4],
                                        self.eventos[5], 
                                        self.eventos[6]]
                else:
                    self.eventos = [self.eventos[0],
                                    self.eventos[1],
                                    [rnd_llegada_handball, llegada_handball, self.reloj + llegada_handball],
                                    self.eventos[3],
                                    self.eventos[4],
                                    self.eventos[5], 
                                    self.eventos[6]]
            elif self.reloj == self.eventos[3][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de futbol"
                objetos = self.objetos
                for i, obj in enumerate(objetos):
                    if obj.estado is True and obj.nombre == "Futbol":
                        objetos.pop(i)
                self.objetos = objetos
                self.objetos.append(self.personal_limpieza("Personal Limpieza", True, self.reloj))
                self.eventos = [self.eventos[0], 
                                self.eventos[1], 
                                self.eventos[2],
                                [None, None, None], 
                                [None, None, None], 
                                [None, None, None], 
                                [hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]] 
            elif self.reloj == self.eventos[4][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de basquetball"
                objetos = self.objetos
                for i, obj in enumerate(objetos):
                    if obj.estado is True and obj.nombre == "Basquet":
                        objetos.pop(i)
                self.objetos = objetos
                self.objetos.append(self.personal_limpieza("Personal Limpieza", True, self.reloj))
                self.eventos = [self.eventos[0], 
                                self.eventos[1], 
                                self.eventos[2],
                                [None, None, None], 
                                [None, None, None], 
                                [None, None, None], 
                                [hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]] 
            elif self.reloj == self.eventos[5][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de handball"
                objetos = self.objetos
                for i, obj in enumerate(objetos):
                    if obj.estado is True and obj.nombre == "Handball":
                        objetos.pop(i)
                self.objetos = objetos
                self.objetos.append(self.personal_limpieza("Personal Limpieza", True, self.reloj))
                self.eventos = [self.eventos[0], 
                                self.eventos[1], 
                                self.eventos[2],
                                [None, None, None], 
                                [None, None, None], 
                                [None, None, None], 
                                [hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]] 

            elif self.reloj == self.eventos[6][2]:
                if len(self.colaFyH) > 0:
                    cola = self.colaFyH
                    equipo = cola.pop(0)
                    self.colaFyH = cola
                    self.estado_cancha = "Cancha ocupada"
                    if equipo.nombre == "Futbol":
                        rnd_ocupacion_futbol = random.random()
                        fin_ocupacion_futbol = self.distribucion_uniforme(rnd_ocupacion_futbol, fin_ocupacion_futbol_inf,fin_ocupacion_futbol_sup)
                        self.tiempo_espera_futbol += (self.reloj - equipo.hora_llegada)
                        objetos = self.objetos
                        for obj in objetos:
                            if obj.hora_llegada == equipo.hora_llegada and obj.nombre == equipo.nombre:
                                obj.set_estado(True)
                                break
                        self.objetos = objetos
                        self.eventos = [self.eventos[0], 
                                        self.eventos[1], 
                                        self.eventos[2],
                                        [rnd_ocupacion_futbol, fin_ocupacion_futbol, self.reloj + fin_ocupacion_futbol], 
                                        [None, None, None], 
                                        [None, None, None], 
                                        [None, None, None]]
                    elif equipo.nombre == "Handball":
                        rnd_ocupacion_handball = random.random()
                        fin_ocupacion_handball  = self.distribucion_uniforme(rnd_ocupacion_handball, fin_ocupacion_handball_inf,fin_ocupacion_handball_sup)
                        self.tiempo_espera_handball += (self.reloj - equipo.hora_llegada)
                        objetos = self.objetos
                        for obj in objetos:
                            if obj.hora_llegada == equipo.hora_llegada and obj.nombre == equipo.nombre:
                                obj.set_estado(True)
                                break
                        self.objetos = objetos
                        self.eventos = [self.eventos[0],
                                        self.eventos[1],
                                        self.eventos[2],
                                        [None, None, None],
                                        [None, None, None],
                                        [rnd_ocupacion_handball, fin_ocupacion_handball, self.reloj + fin_ocupacion_handball], 
                                        [None, None, None]]
                elif len(self.colaB) > 0:
                    cola = self.colaB
                    equipo = cola.pop(0)
                    self.colaB = cola
                    self.estado_cancha = "Cancha ocupada"
                    rnd_ocupacion_basquet = random.random()
                    fin_ocupacion_basquet  = self.distribucion_uniforme(rnd_ocupacion_basquet, fin_ocupacion_basquet_inf,fin_ocupacion_basquet_sup)
                    objetos = self.objetos
                    for obj in objetos:
                        if obj.hora_llegada == equipo.hora_llegada and obj.nombre == equipo.nombre:
                            obj.set_estado(True)
                            break
                    self.objetos = objetos
                    self.tiempo_espera_basquetball += (self.reloj - equipo.hora_llegada)
                    self.eventos = [self.eventos[0], 
                                    self.eventos[1], 
                                    self.eventos[2],
                                    [None, None, None], 
                                    [rnd_ocupacion_basquet, fin_ocupacion_basquet, self.reloj + fin_ocupacion_basquet], 
                                    [None, None, None], [None, None, None]]
                else:
                    self.estado_cancha = "Cancha Libre"
                    self.eventos = [self.eventos[0], 
                                    self.eventos[1], 
                                    self.eventos[2],
                                    [None, None, None], 
                                    [None, None, None], 
                                    [None, None, None], 
                                    [None, None, None]]
                objetos = self.objetos
                for i, obj in enumerate(objetos):
                    if obj.estado is True and obj.nombre == "Personal Limpieza":
                        objetos.pop(i)
                self.objetos = objetos 
                self.nombre_evento = "Fin de limpieza cancha"
                self.tiempo_espera_ocupacion_limpieza += tiempo_demora_limpieza
            return [self.reloj, self.eventos, self.estado_cancha, self.colaB, self.colaFyH, self.tiempo_espera_futbol, self.tiempo_espera_basquetball, self.tiempo_espera_handball, self.tiempo_espera_ocupacion_limpieza, self.objetos]
    def __str__(self):
        obj1 = ""
        obj2 = ""
        obj3 = ""
        obj4 = ""
        if len(self.objetos) > 0:
            if len(self.objetos) == 1:
                obj1 = str(self.objetos[0])
            elif len(self.objetos) == 2:
                obj1 = str(self.objetos[0])
                obj2 = str(self.objetos[1])
            elif len(self.objetos) == 3:
                obj1 = str(self.objetos[0])
                obj2 = str(self.objetos[1])
                obj3 = str(self.objetos[2])
            elif len(self.objetos) == 4:
                obj1 = str(self.objetos[0])
                obj2 = str(self.objetos[1])
                obj3 = str(self.objetos[2])
                obj4 = str(self.objetos[3])
        return f"Nombre del evento: {self.nombre_evento}, Reloj: {self.reloj}, Eventos: {self.eventos}, Estado: {self.estado_cancha}, ColaB: {self.colaB}, ColaFyH: {self.colaFyH}, Objetos1: {obj1}, Objeto2: {obj2}, Objeto3: {obj3}, Objeto4: {obj4}\n"
    #self.objetos[0] if len(self.objetos) > 0 else[]
