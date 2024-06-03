import tkinter as tk
from tkinter import ttk
import random
import heapq
import math
class Fila:
    def __init__(self, id, reloj=0.0, eventos=[], estado_cancha="Cancha Libre", colaB=[], colaFyH=[],tiempo_espera_futbol=0, tiempo_espera_basquetball=0, tiempo_espera_handball=0, tiempo_espera_ocupacion_limpieza=0) -> None:
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
        self.objetos = []
    
    def distribucion_exponencial(self, rnd, media):
        return (-1 * media) * math.log(1 - rnd)
    
    def distribucion_uniforme(self, rnd, inf, sup):
        return inf + (sup - inf) * rnd
    def simular(self, datos, reloj_anterior=0, eventos=[], estado_cancha="", colaB=[], colaFyH=[], tiempo_espera_futbol=0, tiempo_espera_basquetball=0, tiempo_espera_handball=0, tiempo_espera_ocupacion_limpieza=0):
        
        [tiempo_total, tiempo_demora_limpieza, media_llegada_futbol, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup, 
                 intervalo_llegada_handball_inf, intervalo_llegada_handball_sup, fin_ocupacion_futbol_inf, fin_ocupacion_futbol_sup,
                 fin_ocupacion_basquet_inf, fin_ocupacion_basquet_sup, fin_ocupacion_handball_inf, fin_ocupacion_handball_sup, cantidad_equipos_max] = datos
        self.eventos = eventos
        self.reloj = min((evento[2] for evento in self.eventos if evento[2] is not None), default=None)
        print(self.eventos)
        print(self.reloj)
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
                            [[None, None, None]], [[None, None, None]], [[None, None, None]], [[None, None, None]]]
            return [self.reloj, self.eventos, self.estado_cancha, self.colaB, self.colaFyH, self.tiempo_espera_futbol, self.tiempo_espera_basquetball, self.tiempo_espera_handball, self.tiempo_espera_ocupacion_limpieza]
        else:
            self.tiempo_espera_basquetball = tiempo_espera_basquetball
            self.tiempo_espera_futbol = tiempo_espera_futbol
            self.tiempo_espera_handball = tiempo_espera_handball
            self.tiempo_espera_ocupacion_limpieza = tiempo_espera_ocupacion_limpieza
            self.eventos = eventos
            #self.reloj = min(self.eventos[0][2], self.eventos[1][2], self.eventos[2][2], self.eventos[3][2], self.eventos[4][2], self.eventos[5][2], self.eventos[6][2])

            self.colaB = colaB
            self.colaFyH = colaFyH
            self.estado_cancha = estado_cancha
            if self.reloj == self.eventos[0][2]:
                rnd_llegada_futbol = random.random()
                llegada_futbol = self.distribucion_exponencial(rnd_llegada_futbol, media_llegada_futbol)
                self.nombre_evento = "Llegada Equipo de Futbol"
                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                    rnd_ocupacion_futbol = random.Random()
                    fin_ocupacion_futbol = self.distribucion_uniforme(rnd_ocupacion_futbol, fin_ocupacion_futbol_inf,fin_ocupacion_futbol_sup)
                    self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                            [self.eventos[1]], 
                            [self.eventos[2]],
                            [rnd_ocupacion_futbol, fin_ocupacion_futbol, self.reloj + fin_ocupacion_futbol], 
                            [self.eventos[4]], [self.eventos[5]], [self.eventos[6]]]
                else:
                    self.colaFyH.append("Futbol")
            elif self.reloj == self.eventos[1][2]:
                rnd_llegada_basquet = random.random()
                llegada_basquet = self.distribucion_uniforme(rnd_llegada_basquet, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup)
                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                    rnd_ocupacion_basquet = random.Random()
                    fin_ocupacion_basquet  = self.distribucion_uniforme(rnd_ocupacion_basquet, fin_ocupacion_basquet_inf,fin_ocupacion_basquet_sup)
                    self.eventos = [[self.eventos[0]], 
                            [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                            [self.eventos[2]],
                            [self.eventos[3]], 
                            [rnd_ocupacion_basquet, fin_ocupacion_basquet, self.reloj + fin_ocupacion_basquet], 
                            [self.eventos[5]], [self.eventos[6]]]
                else:
                    self.colaB.append("Basquet")
                self.nombre_evento = "Llegada Equipo de BasquetBall"
            elif self.reloj == self.eventos[2][2]:
                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                else:
                    self.colaFyH.append("Handball")
                rnd_llegada_handball = random.random()
                llegada_handball = self.distribucion_uniforme(rnd_llegada_handball, intervalo_llegada_handball_inf, intervalo_llegada_handball_sup)
                ################

                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                    rnd_ocupacion_handball = random.Random()
                    fin_ocupacion_handball  = self.distribucion_uniforme(rnd_ocupacion_handball, fin_ocupacion_handball_inf,fin_ocupacion_handball_sup)
                    self.eventos = [[self.eventos[0]],
                            [self.eventos[1]],
                            [rnd_llegada_handball, llegada_handball, self.reloj + llegada_handball],
                            [self.eventos[3]],
                            [self.eventos[4]],
                            [rnd_ocupacion_handball, fin_ocupacion_handball, self.reloj + fin_ocupacion_handball], 
                            [self.eventos[6]]]
                else:
                    self.colaB.append("Hanball")
                self.nombre_evento = "Llegada Equipo de Hanball"
                ################
            elif self.reloj == self.eventos[3][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de futbol"
                self.eventos = [[self.eventos[0]], 
                            [self.eventos[1]], 
                            [self.eventos[2]],
                            [self.eventos[3]], 
                            [self.eventos[4]], 
                            [self.eventos[5]], 
                            [[hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]]] 
            elif self.reloj == self.eventos[4][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de basquetball"
                self.eventos = [[self.eventos[0]], 
                            [self.eventos[1]], 
                            [self.eventos[2]],
                            [self.eventos[3]], 
                            [self.eventos[4]], 
                            [self.eventos[5]], 
                            [[hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]]] 
            elif self.reloj == self.eventos[5][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de handball"
                self.eventos = [[self.eventos[0]], 
                            [self.eventos[1]], 
                            [self.eventos[2]],
                            [self.eventos[3]], 
                            [self.eventos[4]], 
                            [self.eventos[5]], 
                            [[hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]]] 

            elif self.reloj == self.eventos[6][2]:
                if len(self.colaFyH) > 0:
                    self.colaFyH.pop(0)
                    self.estado_cancha = "Cancha Ocupada"
                elif len(self.colaB) > 0:
                    self.colaB.pop(0)
                    self.estado_cancha = "Cancha Ocupada"
                else:
                    self.estado_cancha = "Cancha Libre"
                self.tiempo_espera_ocupacion_limpieza += (self.reloj - reloj_anterior)
            return [self.reloj, self.eventos, self.estado_cancha, self.colaB, self.colaFyH, self.tiempo_espera_futbol, self.tiempo_espera_basquetball, self.tiempo_espera_handball, self.tiempo_espera_ocupacion_limpieza]
    def __str__(self):
        return f"Nombre del evento: {self.nombre_evento}, Reloj: {self.reloj}, Eventos: {self.eventos}, Estado: {self.estado_cancha}, ColaB: {self.colaB}, ColaFyH: {self.colaFyH}"
class VentanaSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Problemas de Colas")

        # Crear un marco para contener los widgets
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Crear y colocar los widgets de entrada
        self.create_widgets()

    def truncar(self, numero):
        return int(numero * 100) / 100

    def create_widgets(self):
        labels_text = [
            "Cantidad de tiempo (X):", "Tiempo de demora de limpieza:(min)", "Media de llegada de equipo de fútbol:(hs)",
            "Intervalo inferior de llegada de equipo de básquet:(hs)", "Intervalo superior de llegada de equipo de básquet:(hs)",
            "Intervalo inferior de llegada de equipo de handball:(hs)", "Intervalo superior de llegada de equipo de handball:(hs)",
            "Intervalo inferior de fin de ocupación de equipo de fútbol:(min)", "Intervalo superior de fin de ocupación de equipo de fútbol:(min)",
            "Intervalo inferior de fin de ocupación de equipo de básquet:(min)", "Intervalo superior de fin de ocupación de equipo de básquet:(min)",
            "Intervalo inferior de fin de ocupación de equipo de handball:(min)", "Intervalo superior de fin de ocupación de equipo de handball:(min)",
            "Cantidad de equipos en cola máxima:", "Cantidad de filas a mostrar (I):", "Hora específica a mostrar (J):"
        ]
        default_values = [1000, 10, 10, 6, 10, 10, 14, 80, 100, 70, 130, 60, 100, 5, 100, 0]
        self.entries = []
        for i, (text, default) in enumerate(zip(labels_text, default_values)):
            ttk.Label(self.frame, text=text).grid(column=0, row=i, sticky=tk.W)
            entry = ttk.Entry(self.frame)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E))
            entry.insert(0, str(default))
            self.entries.append(entry)

        # Botón para iniciar la simulación
        ttk.Button(self.frame, text="Iniciar Simulación", command=self.iniciar_simulacion).grid(column=1, row=len(labels_text), sticky=tk.E)

        # Configuración para que los widgets se ajusten al tamaño de la ventana
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def iniciar_simulacion(self):
        # Obtener los valores de los campos de entrada
        params = [entry.get() for entry in self.entries]
        tiempo_total = int(params[0])
        tiempo_demora_limpieza = self.truncar(float(params[1]) / 60)
        media_llegada_futbol = float(params[2])
        intervalo_llegada_basquet_inf = float(params[3])
        intervalo_llegada_basquet_sup = float(params[4])
        intervalo_llegada_handball_inf = float(params[5])
        intervalo_llegada_handball_sup = float(params[6])
        fin_ocupacion_futbol_inf = self.truncar(float(params[7]) / 60)
        fin_ocupacion_futbol_sup = self.truncar(float(params[8]) / 60)
        fin_ocupacion_basquet_inf = self.truncar(float(params[9]) / 60)
        fin_ocupacion_basquet_sup = self.truncar(float(params[10]) / 60)
        fin_ocupacion_handball_inf = self.truncar(float(params[11]) / 60)
        fin_ocupacion_handball_sup = self.truncar(float(params[12]) / 60)
        cantidad_equipos_max = int(params[13])
        cantidad_filas = int(params[14])
        hora_especifica = int(params[15])
        
        datos = [tiempo_total, tiempo_demora_limpieza, media_llegada_futbol, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup, 
                 intervalo_llegada_handball_inf, intervalo_llegada_handball_sup, fin_ocupacion_futbol_inf, fin_ocupacion_futbol_sup,
                 fin_ocupacion_basquet_inf, fin_ocupacion_basquet_sup, fin_ocupacion_handball_inf, fin_ocupacion_handball_sup, cantidad_equipos_max]
        tabla = []
        for i in range(cantidad_filas):
            if i == 0:
                fila = Fila(i+1)
                reloj_anterior, eventos, estado_cancha, colaB, colaFyH, tiempo_espera_futbol, tiempo_espera_basquetball, tiempo_espera_handball, tiempo_espera_ocupacion_limpieza = fila.simular(datos)
                tabla.append(fila)
            else:
                fila = Fila(i+1)
                reloj_anterior, eventos, estado_cancha, colaB, colaFyH, tiempo_espera_futbol, tiempo_espera_basquetball, tiempo_espera_handball, tiempo_espera_ocupacion_limpieza = fila.simular(datos, reloj_anterior, eventos, estado_cancha, colaB, colaFyH, tiempo_espera_futbol, tiempo_espera_basquetball, tiempo_espera_handball, tiempo_espera_ocupacion_limpieza)
                tabla.append(fila)

        for fila in tabla:
            print(fila)
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()

