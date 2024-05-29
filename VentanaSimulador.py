import tkinter as tk
from tkinter import ttk
import simpy
import random
import numpy as np


class VentanaSimulador:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Problemas de Colas")

        # Crear un marco para contener los widgets
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Crear y colocar los widgets de entrada
        self.create_widgets()

    def create_widgets(self):
        labels_text = [
            "Cantidad de tiempo (X):", "Tiempo de demora de limpieza:",
            "Media de llegada de equipo de fútbol:",
            "Media de llegada de equipo de básquet:", "Desviación estándar de llegada de equipo de básquet:",
            "Media de llegada de equipo de handball:", "Desviación estándar de llegada de equipo de handball:",
            "Intervalo inferior de ocupación de equipo de fútbol:", "Intervalo superior de ocupación de equipo de fútbol:",
            "Intervalo inferior de ocupación de equipo de básquet:", "Intervalo superior de ocupación de equipo de básquet:",
            "Intervalo inferior de ocupación de equipo de handball:", "Intervalo superior de ocupación de equipo de handball:",
            "Cantidad de equipos en cola máxima:", "Cantidad de filas a mostrar (I):", "Hora específica a mostrar (J):",
            "Cantidad de iteraciones (N):"
        ]

        default_values = [
            1000, 10, 10, 8, 2, 12, 2, 80, 100, 70, 130, 60, 100, 5, 10, 500, 10
        ]

        self.entries = []
        for i, (text, default) in enumerate(zip(labels_text, default_values)):
            ttk.Label(self.frame, text=text).grid(column=0, row=i * 2, sticky=tk.W)
            entry = ttk.Entry(self.frame)
            entry.grid(column=1, row=i * 2, sticky=(tk.W, tk.E))
            entry.insert(0, str(default))  # Insertar valor por defecto
            self.entries.append(entry)

        # Botón para iniciar la simulación
        ttk.Button(self.frame, text="Iniciar Simulación", command=self.iniciar_simulacion).grid(column=1,
                                                                                                row=len(labels_text) * 2,
                                                                                                sticky=tk.E)

        # Configuración para que los widgets se ajusten al tamaño de la ventana
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def iniciar_simulacion(self):
        # Obtener los valores de los campos de entrada
        params = [entry.get() for entry in self.entries]
        tiempo_total = int(params[0])
        tiempo_demora_limpieza = int(params[1])
        media_llegada_futbol = float(params[2])
        media_llegada_basquet = float(params[3])
        desviacion_llegada_basquet = float(params[4])
        media_llegada_handball = float(params[5])
        desviacion_llegada_handball = float(params[6])
        ocupacion_futbol_inf = int(params[7])
        ocupacion_futbol_sup = int(params[8])
        ocupacion_basquet_inf = int(params[9])
        ocupacion_basquet_sup = int(params[10])
        ocupacion_handball_inf = int(params[11])
        ocupacion_handball_sup = int(params[12])
        cantidad_equipos_max = int(params[13])
        cantidad_filas = int(params[14])
        hora_especifica = int(params[15])
        cantidad_iteraciones = int(params[16])

        # Llamar a la función de simulación con los parámetros obtenidos
        resultados_simulacion = self.simular(tiempo_total, tiempo_demora_limpieza, media_llegada_futbol,
                                             media_llegada_basquet, desviacion_llegada_basquet, media_llegada_handball,
                                             desviacion_llegada_handball, ocupacion_futbol_inf, ocupacion_futbol_sup,
                                             ocupacion_basquet_inf, ocupacion_basquet_sup, ocupacion_handball_inf,
                                             ocupacion_handball_sup, cantidad_equipos_max, cantidad_iteraciones,
                                             cantidad_filas, hora_especifica)

        # Mostrar resultados en una nueva ventana
        self.mostrar_resultados(resultados_simulacion, cantidad_filas, hora_especifica)

    def simular(self, tiempo_total, tiempo_demora_limpieza, media_llegada_futbol, media_llegada_basquet,
                desviacion_llegada_basquet, media_llegada_handball, desviacion_llegada_handball, ocupacion_futbol_inf,
                ocupacion_futbol_sup, ocupacion_basquet_inf, ocupacion_basquet_sup, ocupacion_handball_inf,
                ocupacion_handball_sup, cantidad_equipos_max, cantidad_iteraciones, cantidad_filas, hora_especifica):
        resultados_simulacion = []
        iteraciones = 0

        def llegada_grupo(env, tipo, distribucion_llegada, ocupacion_inf, ocupacion_sup, tiempos_espera,
                          tiempo_limpieza_ocupado):
            nonlocal iteraciones
            while env.now < tiempo_total and iteraciones < 100000:
                next_arrival = distribucion_llegada()
                yield env.timeout(next_arrival)
                grupo_id = f'{tipo}_{env.now}'
                tiempos_espera[tipo].append(env.now)
                evento = {'hora': env.now, 'evento': f'Llega {grupo_id}', 'estado': 'espera'}

                if tipo == 'futbol':
                    evento['random_futbol'] = next_arrival
                    evento['tiempo_entre_llegadas_futbol'] = next_arrival
                    evento['proxima_llegada_futbol'] = env.now + next_arrival
                elif tipo == 'basquet':
                    evento['random_basquet'] = next_arrival
                    evento['tiempo_entre_llegadas_basquet'] = next_arrival
                    evento['proxima_llegada_basquet'] = env.now + next_arrival
                elif tipo == 'handball':
                    evento['random_handball'] = next_arrival
                    evento['tiempo_entre_llegadas_handball'] = next_arrival
                    evento['proxima_llegada_handball'] = env.now + next_arrival

                resultados_simulacion.append(evento)
                with cancha.request(priority=prioridad(tipo)) as turno:
                    yield turno
                    duracion_ocupacion = random.randint(ocupacion_inf, ocupacion_sup)
                    evento = {'hora': env.now, 'evento': f'Entra {grupo_id}', 'duracion': duracion_ocupacion,
                              'estado': 'ocupado'}
                    resultados_simulacion.append(evento)
                    yield env.timeout(duracion_ocupacion)
                    tiempo_limpieza_ocupado.append(env.now)
                    with limpieza.request() as limpieza_turno:
                        yield limpieza_turno
                        yield env.timeout(tiempo_demora_limpieza)
                        evento = {'hora': env.now, 'evento': f'Limpieza cancha',
                                  'tiempo_limpieza': tiempo_demora_limpieza,
                                  'proxima_limpieza': env.now + tiempo_demora_limpieza, 'estado': 'limpieza'}
                        resultados_simulacion.append(evento)
                iteraciones += 1

        def prioridad(tipo):
            if (tipo == 'handball' and (env.now not in tiempos_espera['futbol']) and (
                    env.now not in tiempos_espera['basquet'])):
                return 2
            return 1

        for _ in range(cantidad_iteraciones):
            # Crear el entorno de simulación
            env = simpy.Environment()

            # Crear los recursos y contenedores para las estadísticas
            cancha = simpy.PriorityResource(env, capacity=1)
            limpieza = simpy.Resource(env, capacity=1)
            tiempos_espera = {'futbol': [], 'basquet': [], 'handball': []}
            tiempo_limpieza_ocupado = []

            # Iniciar los procesos de llegada de los diferentes tipos de grupos
            env.process(llegada_grupo(env, 'futbol', lambda: random.expovariate(1 / media_llegada_futbol),
                                      ocupacion_futbol_inf, ocupacion_futbol_sup, tiempos_espera,
                                      tiempo_limpieza_ocupado))
            env.process(llegada_grupo(env, 'basquet', lambda: random.gauss(media_llegada_basquet,
                                                                           desviacion_llegada_basquet),
                                      ocupacion_basquet_inf, ocupacion_basquet_sup, tiempos_espera,
                                      tiempo_limpieza_ocupado))
            env.process(llegada_grupo(env, 'handball', lambda: random.gauss(media_llegada_handball,
                                                                            desviacion_llegada_handball),
                                      ocupacion_handball_inf, ocupacion_handball_sup, tiempos_espera,
                                      tiempo_limpieza_ocupado))

            # Ejecutar la simulación
            env.run(until=tiempo_total)

        return resultados_simulacion

    def mostrar_resultados(self, resultados, cantidad_filas, hora_especifica):
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(self.root)
        ventana_resultados.title("Resultados de la Simulación")

        # Crear un frame para contener el Treeview y las Scrollbars
        frame_tree = ttk.Frame(ventana_resultados)
        frame_tree.pack(fill=tk.BOTH, expand=True)

        # Crear un Treeview para mostrar los resultados
        tree = ttk.Treeview(frame_tree, columns=(
            "Evento", "Hora", "Tiempo entre llegadas Futbol", "Próxima llegada Futbol",
            "Tiempo entre llegadas Basquet", "Próxima llegada Basquet",
            "Tiempo entre llegadas Handball", "Próxima llegada Handball",
            "Tiempo de limpieza", "Próxima limpieza",
            "Estado", "Espera Futbol", "Espera Basquet", "Espera Handball"
        ), show="headings")

        # Definir los encabezados
        tree.heading("Evento", text="Evento")
        tree.heading("Hora", text="Hora")
        tree.heading("Tiempo entre llegadas Futbol", text="Tiempo entre llegadas Futbol")
        tree.heading("Próxima llegada Futbol", text="Próxima llegada Futbol")
        tree.heading("Tiempo entre llegadas Basquet", text="Tiempo entre llegadas Basquet")
        tree.heading("Próxima llegada Basquet", text="Próxima llegada Basquet")
        tree.heading("Tiempo entre llegadas Handball", text="Tiempo entre llegadas Handball")
        tree.heading("Próxima llegada Handball", text="Próxima llegada Handball")
        tree.heading("Tiempo de limpieza", text="Tiempo de limpieza")
        tree.heading("Próxima limpieza", text="Próxima limpieza")
        tree.heading("Estado", text="Estado")
        tree.heading("Espera Futbol", text="Espera Futbol")
        tree.heading("Espera Basquet", text="Espera Basquet")
        tree.heading("Espera Handball", text="Espera Handball")

        # Definir los anchos de las columnas
        for col in tree["columns"]:
            tree.column(col, minwidth=100, width=150)

        # Añadir datos simulados al Treeview
        for dato in resultados[:cantidad_filas]:  # Mostrar solo las primeras `cantidad_filas` filas
            tree.insert("", tk.END, values=(
                dato.get('evento', ''), dato.get('hora', ''),
                dato.get('tiempo_entre_llegadas_futbol', ''), dato.get('proxima_llegada_futbol', ''),
                dato.get('tiempo_entre_llegadas_basquet', ''), dato.get('proxima_llegada_basquet', ''),
                dato.get('tiempo_entre_llegadas_handball', ''), dato.get('proxima_llegada_handball', ''),
                dato.get('tiempo_limpieza', ''), dato.get('proxima_limpieza', ''),
                dato.get('estado', ''), dato.get('espera_futbol', ''), dato.get('espera_basquet', ''),
                dato.get('espera_handball', '')
            ))

        # Añadir Scrollbars
        hsb = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
        vsb = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
        tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        # Mostrar la hora específica si está en los resultados
        resultados_hora_especifica = [dato for dato in resultados if dato.get('hora', None) == hora_especifica]
        if resultados_hora_especifica:
            label_hora_especifica = ttk.Label(ventana_resultados, text=f"Resultados para la hora específica {hora_especifica}:")
            label_hora_especifica.pack(pady=10)
            for dato in resultados_hora_especifica:
                ttk.Label(ventana_resultados, text=str(dato)).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()

