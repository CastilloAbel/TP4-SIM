import tkinter as tk
from tkinter import Toplevel, ttk
from tkinter import Scrollbar
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
                                "rnd_b", "llegada_b","proxima_b", "rnd_h", "llegada_h","proxima_h",
                                "rnd_cancha_f", "ocupacion_cancha_f","fin_ocupacion_f",
                                "rnd_cancha_b", "ocupacion_cancha_b","fin_ocupacion_b",
                                "rnd_cancha_h", "ocupacion_cancha_h","fin_ocupacion_h",
                                "tiempo_actual", "demora_limpieza", "fin_limpieza",
                                "Estado Cancha", "ColaB", "ColaFyH","Tiempo_espera_f",
                                "Tiempo_espera_h","Tiempo_espera_b","Tiempo_ocupacion_limpieza" ,"Objeto1", "Objeto2", "Objeto3", "Objeto4"), show="headings")
        
        # Configurar encabezados y anchos de columna
        columns = [
            ("ID", 50), ("Evento", 270), ("Reloj", 90), ("rnd_f", 80), ("llegada_f", 80), ("proxima_f", 80),
            ("rnd_b", 80), ("llegada_b", 80), ("proxima_b", 80), ("rnd_h", 80), ("llegada_h", 80), ("proxima_h", 80),
            ("rnd_cancha_f", 80), ("ocupacion_cancha_f", 120), ("fin_ocupacion_f", 120),
            ("rnd_cancha_b", 80), ("ocupacion_cancha_b", 120), ("fin_ocupacion_b", 120),
            ("rnd_cancha_h", 80), ("ocupacion_cancha_h", 120), ("fin_ocupacion_h", 120),
            ("tiempo_actual", 80), ("demora_limpieza", 120), ("fin_limpieza", 80),
            ("Estado Cancha", 120), ("ColaB", 60), ("ColaFyH", 60),("Tiempo_espera_f",120),
            ("Tiempo_espera_h",120),("Tiempo_espera_b",120),("Tiempo_ocupacion_limpieza",160),
            ("Objeto1", 480),("Objeto2", 480),("Objeto3", 480),("Objeto4", 480)
        ]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=width, width=width, anchor='center')
    
        self.tree.column("Estado Cancha", width=120, anchor='w')
        self.tree.column("Evento", width=270, anchor='w')
        self.tree.column("Objeto1", width=480, anchor='w')
        self.tree.column("Objeto2", width=480, anchor='w')
        self.tree.column("Objeto3", width=480, anchor='w')
        self.tree.column("Objeto4", width=480, anchor='w')

        # Crear los scrollbars y asociarlos con el Treeview
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        # Empaquetar el Treeview y los scrollbars
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(expand=True, fill=tk.BOTH)



    def mostrar_resultados(self, tabla_resultados, hora_especifica, cantidad_filas, colas, objetos, estados):

        # Truncar
        def truncar(numero, decimales=3):
            if numero is not None:
                factor = 10 ** decimales
                return int(numero * factor) / factor
            else:
                return ""
            
        # Limpiar el Treeview antes de insertar nuevos datos
        for row in self.tree.get_children():
            self.tree.delete(row)

        if hora_especifica == 0 and cantidad_filas != 0:
            for i, fila in enumerate(tabla_resultados[0:cantidad_filas]):
                objeto1, objeto2, objeto3, objeto4 = "", "", "", ""
                if len(objetos[fila.id]) > 0:
                    if len(objetos[fila.id]) == 1:
                        o1 = objetos.get(fila.id)[0]
                        o1.set_estado(estados[fila.id][0])
                        objeto1 = str(o1)
                    elif len(objetos[fila.id]) == 2:
                        o1 = objetos.get(fila.id)[0]
                        o1.set_estado(estados[fila.id][0])
                        objeto1 = str(o1)
                        o2 = objetos.get(fila.id)[1]
                        o2.set_estado(estados[fila.id][1])
                        objeto2 = str(o2)
                    elif len(objetos[fila.id]) == 3:
                        o1 = objetos.get(fila.id)[0]
                        o1.set_estado(estados[fila.id][0])
                        objeto1 = str(o1)
                        o2 = objetos.get(fila.id)[1]
                        o2.set_estado(estados[fila.id][1])
                        objeto2 = str(o2)
                        o3 = objetos.get(fila.id)[2]
                        o3.set_estado(estados[fila.id][2])
                        objeto3 = str(o3)
                    else:
                        o1 = objetos.get(fila.id)[0]
                        o1.set_estado(estados[fila.id][0])
                        objeto1 = str(o1)
                        o2 = objetos.get(fila.id)[1]
                        o2.set_estado(estados[fila.id][1])
                        objeto2 = str(o2)
                        o3 = objetos.get(fila.id)[2]
                        o3.set_estado(estados[fila.id][2])
                        objeto3 = str(o3)
                        o4 = objetos.get(fila.id)[3]
                        o4.set_estado(estados[fila.id][3])
                        objeto4 = str(o4)
                
                self.tree.insert("", "end", values=(fila.id, fila.nombre_evento, truncar(fila.reloj),
                                truncar(fila.eventos[0][0]), truncar(fila.eventos[0][1]),truncar(fila.eventos[0][2]), 
                                truncar(fila.eventos[1][0]), truncar(fila.eventos[1][1]),truncar(fila.eventos[1][2]),
                                truncar(fila.eventos[2][0]), truncar(fila.eventos[2][1]),truncar(fila.eventos[2][2]),
                                truncar(fila.eventos[3][0]),truncar(fila.eventos[3][1]), truncar(fila.eventos[3][2]),
                                truncar(fila.eventos[4][0]),truncar(fila.eventos[4][1]), truncar(fila.eventos[4][2]),
                                truncar(fila.eventos[5][0]),truncar(fila.eventos[5][1]), truncar(fila.eventos[5][2]),
                                truncar(fila.eventos[6][0]),truncar(fila.eventos[6][1]), truncar(fila.eventos[6][2]),
                                fila.estado_cancha, colas[i][0], colas[i][1], truncar(fila.tiempo_espera_futbol),
                                truncar(fila.tiempo_espera_handball), truncar(fila.tiempo_espera_basquetball),
                                truncar(fila.tiempo_espera_ocupacion_limpieza),objeto1, objeto2, objeto3, objeto4))
            self.tree.insert("", "end", values=(tabla_resultados[-1].id, tabla_resultados[-1].nombre_evento, truncar(tabla_resultados[-1].reloj),
                            truncar(tabla_resultados[-1].eventos[0][0]), truncar(tabla_resultados[-1].eventos[0][1]), truncar(tabla_resultados[-1].eventos[0][2]), 
                            truncar(tabla_resultados[-1].eventos[1][0]), truncar(tabla_resultados[-1].eventos[1][1]), truncar(tabla_resultados[-1].eventos[1][2]),
                            truncar(tabla_resultados[-1].eventos[2][0]), truncar(tabla_resultados[-1].eventos[2][1]), truncar(tabla_resultados[-1].eventos[2][2]),
                            truncar(tabla_resultados[-1].eventos[3][0]), truncar(tabla_resultados[-1].eventos[3][1]), truncar(tabla_resultados[-1].eventos[3][2]),
                            truncar(tabla_resultados[-1].eventos[4][0]), truncar(tabla_resultados[-1].eventos[4][1]), truncar(tabla_resultados[-1].eventos[4][2]),
                            truncar(tabla_resultados[-1].eventos[5][0]), truncar(tabla_resultados[-1].eventos[5][1]), truncar(tabla_resultados[-1].eventos[5][2]),
                            truncar(tabla_resultados[-1].eventos[6][0]), truncar(tabla_resultados[-1].eventos[6][1]), truncar(tabla_resultados[-1].eventos[6][2]),
                            tabla_resultados[-1].estado_cancha, colas[-1][0], colas[-1][1], truncar(tabla_resultados[-1].tiempo_espera_futbol),
                            truncar(tabla_resultados[-1].tiempo_espera_handball), truncar(tabla_resultados[-1].tiempo_espera_basquetball),
                            truncar(tabla_resultados[-1].tiempo_espera_ocupacion_limpieza)))

                                                
        elif hora_especifica != 0 and cantidad_filas != 0:

            for i, fila in enumerate(tabla_resultados[0:cantidad_filas]):
                if fila.reloj >= hora_especifica:
                    objeto1, objeto2, objeto3, objeto4 = "", "", "", ""
                    if len(objetos[fila.id]) > 0:
                        if len(objetos[fila.id]) == 1:
                            objeto1 = str(objetos.get(fila.id)[0])
                        elif len(objetos[fila.id]) == 2:
                            objeto1 = str(objetos.get(fila.id)[0])
                            objeto2 = str(objetos.get(fila.id)[1])
                        elif len(objetos[fila.id]) == 3:
                            objeto1 = str(objetos.get(fila.id)[0])
                            objeto2 = str(objetos.get(fila.id)[1])
                            objeto3 = str(objetos.get(fila.id)[2])
                        else:
                            objeto1 = str(objetos.get(fila.id)[0])
                            objeto2 = str(objetos.get(fila.id)[1])
                            objeto3 = str(objetos.get(fila.id)[2])
                            objeto4 = str(objetos.get(fila.id)[3])
                
                    self.tree.insert("", "end", values=(fila.id, fila.nombre_evento, truncar(fila.reloj),
                                    truncar(fila.eventos[0][0]), truncar(fila.eventos[0][1]), truncar(fila.eventos[0][2]), 
                                    truncar(fila.eventos[1][0]), truncar(fila.eventos[1][1]), truncar(fila.eventos[1][2]),
                                    truncar(fila.eventos[2][0]), truncar(fila.eventos[2][1]), truncar(fila.eventos[2][2]),
                                    truncar(fila.eventos[3][0]), truncar(fila.eventos[3][1]), truncar(fila.eventos[3][2]),
                                    truncar(fila.eventos[4][0]), truncar(fila.eventos[4][1]), truncar(fila.eventos[4][2]),
                                    truncar(fila.eventos[5][0]), truncar(fila.eventos[5][1]), truncar(fila.eventos[5][2]),
                                    truncar(fila.eventos[6][0]), truncar(fila.eventos[6][1]), truncar(fila.eventos[6][2]),
                                    fila.estado_cancha, colas[i][0], colas[i][1], truncar(fila.tiempo_espera_futbol),
                                    truncar(fila.tiempo_espera_handball), truncar(fila.tiempo_espera_basquetball),
                                    truncar(fila.tiempo_espera_ocupacion_limpieza), objeto1, objeto2, objeto3, objeto4))
            self.tree.insert("", "end", values=(tabla_resultados[-1].id, tabla_resultados[-1].nombre_evento, truncar(fila.reloj),
                            truncar(tabla_resultados[-1].eventos[0][0]), truncar(tabla_resultados[-1].eventos[0][1]), truncar(tabla_resultados[-1].eventos[0][2]), 
                            truncar(tabla_resultados[-1].eventos[1][0]), truncar(tabla_resultados[-1].eventos[1][1]), truncar(tabla_resultados[-1].eventos[1][2]),
                            truncar(tabla_resultados[-1].eventos[2][0]), truncar(tabla_resultados[-1].eventos[2][1]), truncar(tabla_resultados[-1].eventos[2][2]),
                            truncar(tabla_resultados[-1].eventos[3][0]), truncar(tabla_resultados[-1].eventos[3][1]), truncar(tabla_resultados[-1].eventos[3][2]),
                            truncar(tabla_resultados[-1].eventos[4][0]), truncar(tabla_resultados[-1].eventos[4][1]), truncar(tabla_resultados[-1].eventos[4][2]),
                            truncar(tabla_resultados[-1].eventos[5][0]), truncar(tabla_resultados[-1].eventos[5][1]), truncar(tabla_resultados[-1].eventos[5][2]),
                            truncar(tabla_resultados[-1].eventos[6][0]), truncar(tabla_resultados[-1].eventos[6][1]), truncar(tabla_resultados[-1].eventos[6][2]),
                            tabla_resultados[-1].estado_cancha, colas[-1][0], colas[-1][1], truncar(tabla_resultados[-1].tiempo_espera_futbol),
                            truncar(tabla_resultados[-1].tiempo_espera_handball), truncar(tabla_resultados[-1].tiempo_espera_basquetball),
                            truncar(tabla_resultados[-1].tiempo_espera_ocupacion_limpieza)))
        else:
            self.tree.insert("","end",values="")           