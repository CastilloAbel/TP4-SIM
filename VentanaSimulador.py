import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import Scrollbar
import random
import math



class Temporal:
    def __init__(self, nombre, estado, hora_llegada):
        self.nombre = nombre
        self.estado = estado
        self.hora_llegada = hora_llegada

    def set_estado(self, estado):
        self.estado = estado
    
    def __str__(self):
        return f"Nombre:{self.nombre}, Estado:{self.estado}, Hora de llegada:{self.hora_llegada}\n"

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
            return [reloj, self.eventos, self.estado_cancha, [], [], self.tiempo_espera_futbol, self.tiempo_espera_basquetball, self.tiempo_espera_handball, self.tiempo_espera_ocupacion_limpieza]
        else:
            self.reloj = min((evento[2] for evento in self.eventos if evento[2] is not None), default=None)

            #self.reloj = min(self.eventos[0][2], self.eventos[1][2], self.eventos[2][2], self.eventos[3][2], self.eventos[4][2], self.eventos[5][2], self.eventos[6][2])

            if self.reloj == self.eventos[0][2]:
                rnd_llegada_futbol = random.random()
                llegada_futbol = self.distribucion_exponencial(rnd_llegada_futbol, media_llegada_futbol)
                self.nombre_evento = "Llegada Equipo de Futbol"
                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                    self.objetos.append(self.equipo_futbol("Futbol","Jugando", self.reloj))
                    rnd_ocupacion_futbol = random.random()
                    fin_ocupacion_futbol = self.distribucion_uniforme(rnd_ocupacion_futbol, fin_ocupacion_futbol_inf,fin_ocupacion_futbol_sup)
                    self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                            self.eventos[1], 
                            self.eventos[2],
                            [rnd_ocupacion_futbol, fin_ocupacion_futbol, self.reloj + fin_ocupacion_futbol], 
                            self.eventos[4], self.eventos[5], self.eventos[6]]
                else:
                    self.colaFyH.append(self.equipo_futbol("Futbol", "Esperando Jugar", self.reloj))
                    self.eventos = [[rnd_llegada_futbol, llegada_futbol, self.reloj + llegada_futbol], 
                            self.eventos[1], 
                            self.eventos[2],
                            self.eventos[3], 
                            self.eventos[4], self.eventos[5], self.eventos[6]]
            elif self.reloj == self.eventos[1][2]:
                rnd_llegada_basquet = random.random()
                llegada_basquet = self.distribucion_uniforme(rnd_llegada_basquet, intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup)
                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                    self.objetos.append(self.equipo_basquet("Basquet", "Jugando", self.reloj))
                    rnd_ocupacion_basquet = random.random()
                    fin_ocupacion_basquet  = self.distribucion_uniforme(rnd_ocupacion_basquet, fin_ocupacion_basquet_inf,fin_ocupacion_basquet_sup)
                    self.eventos = [self.eventos[0], 
                            [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                            self.eventos[2],
                            self.eventos[3], 
                            [rnd_ocupacion_basquet, fin_ocupacion_basquet, self.reloj + fin_ocupacion_basquet], 
                            self.eventos[5], self.eventos[6]]
                else:
                    self.colaB.append(self.equipo_basquet("Basquet", "Esperando Jugar", self.reloj))
                    self.eventos = [self.eventos[0], 
                            [rnd_llegada_basquet, llegada_basquet, self.reloj + llegada_basquet], 
                            self.eventos[2],
                            self.eventos[3], 
                            self.eventos[4], 
                            self.eventos[5], self.eventos[6]]
                self.nombre_evento = "Llegada Equipo de BasquetBall"
            elif self.reloj == self.eventos[2][2]:
                rnd_llegada_handball = random.random()
                llegada_handball = self.distribucion_uniforme(rnd_llegada_handball, intervalo_llegada_handball_inf, intervalo_llegada_handball_sup)
                if self.estado_cancha == "Cancha Libre":
                    self.estado_cancha = "Cancha ocupada"
                    self.objetos.append(self.equipo_handball("Handball", "Jugando", self.reloj))
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
                    self.colaFyH.append(self.equipo_handball("Handball", "Esperando Jugar", self.reloj))
                    self.eventos = [self.eventos[0],
                            self.eventos[1],
                            [rnd_llegada_handball, llegada_handball, self.reloj + llegada_handball],
                            self.eventos[3],
                            self.eventos[4],
                            self.eventos[5], 
                            self.eventos[6]]
                self.nombre_evento = "Llegada Equipo de Handball"
                ################
            elif self.reloj == self.eventos[3][2]:
                hora_comienzo_limpieza = self.reloj
                self.nombre_evento = "Fin de ocupacion cancha de futbol"
                self.objetos.append(self.personal_limpieza("Personal Limpieza", "Limpiando", self.reloj))
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
                self.objetos.append(self.personal_limpieza("Personal Limpieza", "Limpiando", self.reloj))
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
                self.objetos.append(self.personal_limpieza("Personal Limpieza", "Limpiando", self.reloj))
                self.eventos = [self.eventos[0], 
                            self.eventos[1], 
                            self.eventos[2],
                            [None, None, None], 
                            [None, None, None], 
                            [None, None, None], 
                            [hora_comienzo_limpieza, tiempo_demora_limpieza, self.reloj + tiempo_demora_limpieza]] 

            elif self.reloj == self.eventos[6][2]:
                if len(self.colaFyH) > 0:
                    equipo = self.colaFyH.pop(0)
                    self.estado_cancha = "Cancha Ocupada"
                    if equipo.nombre == "Futbol":
                        rnd_ocupacion_futbol = random.random()
                        fin_ocupacion_futbol = self.distribucion_uniforme(rnd_ocupacion_futbol, fin_ocupacion_futbol_inf,fin_ocupacion_futbol_sup)
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
                        self.eventos = [self.eventos[0],
                                self.eventos[1],
                                self.eventos[2],
                                [None, None, None],
                                [None, None, None],
                                [rnd_ocupacion_handball, fin_ocupacion_handball, self.reloj + fin_ocupacion_handball], 
                                [None, None, None]]
                elif len(self.colaB) > 0:
                    self.colaB.pop(0)
                    self.estado_cancha = "Cancha Ocupada"
                    rnd_ocupacion_basquet = random.random()
                    fin_ocupacion_basquet  = self.distribucion_uniforme(rnd_ocupacion_basquet, fin_ocupacion_basquet_inf,fin_ocupacion_basquet_sup)
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
                self.nombre_evento = "Fin de limpieza cancha"
                self.tiempo_espera_ocupacion_limpieza += tiempo_demora_limpieza
            return [self.reloj, self.eventos, self.estado_cancha, self.colaB, self.colaFyH, self.tiempo_espera_futbol, self.tiempo_espera_basquetball, self.tiempo_espera_handball, self.tiempo_espera_ocupacion_limpieza]
    def __str__(self):
        return f"Nombre del evento: {self.nombre_evento}, Reloj: {self.reloj}, Eventos: {self.eventos}, Estado: {self.estado_cancha}, ColaB: {self.colaB}, ColaFyH: {self.colaFyH}, Objetos:{self.objetos[0] if len(self.objetos) > 0 else[]}\n"

class VentanaSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Problemas de Colas")

        # Crear un marco para contener los widgets
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Crear y colocar los widgets de entrada
        self.create_widgets()

    def truncar(self, numero, decimales=3):
        factor = 10 ** decimales
        return int(numero * factor) / factor
    

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
                lista = fila.simular(datos)
                tabla.append(fila)
            else:
                fila = Fila(i+1, lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6], lista[7], lista[8])
                lista = fila.simular(datos)
                tabla.append(fila)
        
        print(lista[5])
        print(lista[6])
        print(lista[7])
        print(lista[8])

        # Crear una nueva ventana para mostrar los resultados
        root_resultados = tk.Tk()
        resultados_ventana = ResultadosVentana(root_resultados)
        resultados_ventana.mostrar_resultados(tabla, hora_especifica)



class ResultadosVentana:
    def __init__(self, root ):
        self.root = root
        #self.frame = frame
        self.root.title("Resultados de la Simulación")

        # Crear un Frame para contener el Treeview y los scrollbars
        self.frame = ttk.Frame(root)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Crear el Treeview para mostrar los resultados de la simulación
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Evento", "Reloj","rnd_f", "llegada_f","proxima_f", 
                                "rnd_h", "llegada_h","proxima_h", "rnd_b", "llegada_b","proxima_b",
                                "rnd_cancha_f", "ocupacion_cancha_f","fin_ocupacion_f",
                                "rnd_cancha_h", "ocupacion_cancha_h","fin_ocupacion_h",
                                "rnd_cancha_b", "ocupacion_cancha_b","fin_ocupacion_b",
                                "tiempo_actual", "demora_limpieza", "fin_limpieza",
                                "Estado Cancha", "ColaB", "ColaFyH","Tiempo_espera_f",
                                "Tiempo_espera_h","Tiempo_espera_b","Tiempo_ocupacion_limpieza" ,"Objetos"), show="headings")
        
        # Configurar encabezados y anchos de columna
        columns = [
            ("ID", 50), ("Evento", 200), ("Reloj", 150), ("rnd_f", 150), ("llegada_f", 150), ("proxima_f", 150),
            ("rnd_h", 150), ("llegada_h", 150), ("proxima_h", 150), ("rnd_b", 150), ("llegada_b", 150), ("proxima_b", 150),
            ("rnd_cancha_f", 150), ("ocupacion_cancha_f", 150), ("fin_ocupacion_f", 150),
            ("rnd_cancha_h", 150), ("ocupacion_cancha_h", 150), ("fin_ocupacion_h", 150),
            ("rnd_cancha_b", 150), ("ocupacion_cancha_b", 150), ("fin_ocupacion_b", 150),
            ("tiempo_actual", 150), ("demora_limpieza", 150), ("fin_limpieza", 150),
            ("Estado Cancha", 100), ("ColaB", 60), ("ColaFyH", 60),("Tiempo_espera_f",150),
            ("Tiempo_espera_h",150),("Tiempo_espera_b",150),("Tiempo_ocupacion_limpieza",150)
            ,("Objetos", 500)
        ]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
    

        # Crear los scrollbars y asociarlos con el Treeview
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Empaquetar el Treeview y los scrollbars
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(expand=True, fill=tk.BOTH)



    def mostrar_resultados(self, tabla_resultados, hora_especifica):

        def truncar(numero, decimales=3):
            if numero is not None:
                factor = 10 ** decimales
                return int(numero * factor) / factor
            else:
                return ""
                

        # Limpiar el Treeview antes de insertar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insertar los datos en el Treeview

        if hora_especifica == 0:
            for fila in tabla_resultados:
                self.tree.insert("", "end", values=(fila.id, fila.nombre_evento, truncar(fila.reloj),
                                                truncar(fila.eventos[0][0]), truncar(fila.eventos[0][1]),truncar(fila.eventos[0][2]), 
                                                truncar(fila.eventos[1][0]), truncar(fila.eventos[1][1]),truncar(fila.eventos[1][2]),
                                                truncar(fila.eventos[2][0]), truncar(fila.eventos[2][1]),truncar(fila.eventos[2][2]),
                                                truncar(fila.eventos[3][0]),truncar(fila.eventos[3][1]), truncar(fila.eventos[3][2]),
                                                truncar(fila.eventos[4][0]),truncar(fila.eventos[4][1]), truncar(fila.eventos[4][2]),
                                                truncar(fila.eventos[5][0]),truncar(fila.eventos[5][1]), truncar(fila.eventos[5][2]),
                                                truncar(fila.eventos[6][0]),truncar(fila.eventos[6][1]), truncar(fila.eventos[6][2]),
                                                fila.estado_cancha, len(fila.colaB), len(fila.colaFyH), truncar(fila.tiempo_espera_futbol),
                                                truncar(fila.tiempo_espera_handball), truncar(fila.tiempo_espera_basquetball),
                                                truncar(fila.tiempo_espera_ocupacion_limpieza),str(fila.objetos[0]) if len(fila.objetos) > 0 else ""))
                                                
        else:
            for fila in tabla_resultados:
                if fila.reloj >= hora_especifica:
                    self.tree.insert("", "end", values=(fila.id, fila.nombre_evento, truncar(fila.reloj),
                                                truncar(fila.eventos[0][0]), truncar(fila.eventos[0][1]), truncar(fila.eventos[0][2]), 
                                                truncar(fila.eventos[1][0]), truncar(fila.eventos[1][1]), truncar(fila.eventos[1][2]),
                                                truncar(fila.eventos[2][0]), truncar(fila.eventos[2][1]), truncar(fila.eventos[2][2]),
                                                truncar(fila.eventos[3][0]), truncar(fila.eventos[3][1]), truncar(fila.eventos[3][2]),
                                                truncar(fila.eventos[4][0]), truncar(fila.eventos[4][1]), truncar(fila.eventos[4][2]),
                                                truncar(fila.eventos[5][0]), truncar(fila.eventos[5][1]), truncar(fila.eventos[5][2]),
                                                truncar(fila.eventos[6][0]), truncar(fila.eventos[6][1]), truncar(fila.eventos[6][2]),
                                                fila.estado_cancha, len(fila.colaB), len(fila.colaFyH), truncar(fila.tiempo_espera_futbol),
                                                truncar(fila.tiempo_espera_handball), truncar(fila.tiempo_espera_basquetball),
                                                truncar(fila.tiempo_espera_ocupacion_limpieza),str(fila.objetos[0]) if len(fila.objetos) > 0 else ""))

if __name__ == "__main__":
    root = tk.Tk()
    ventana_simulador = VentanaSimulador(root)
    root.mainloop()
    