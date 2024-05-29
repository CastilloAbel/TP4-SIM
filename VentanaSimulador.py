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
            "Cantidad de tiempo (X):", "Tiempo de demora de limpieza:", "Media de llegada de equipo de fútbol:",
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
        for i, text in enumerate(labels_text):
            ttk.Label(self.frame, text=text).grid(column=0, row=i, sticky=tk.W)
            entry = ttk.Entry(self.frame)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E))
            entry.insert(0, str(default_values[i]))  # Insertar valor por defecto
            self.entries.append(entry)

        # Botón para iniciar la simulación
        ttk.Button(self.frame, text="Iniciar Simulación", command=self.iniciar_simulacion).grid(column=1,
                                                                                                row=len(labels_text),
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

        def llegada_grupo(env, tipo, distribucion_llegada, ocupacion_inf, ocupacion_sup, tiempos_espera, tiempo_limpieza_ocupado):
            nonlocal iteraciones
            while env.now < tiempo_total and iteraciones < 100000:
                next_arrival = distribucion_llegada()
                yield env.timeout(next_arrival)
                grupo_id = f'{tipo}_{env.now}'
                tiempos_espera[tipo].append(env.now)
                evento = {'hora': env.now, 'evento': f'Llega {grupo_id}', 'siguiente_evento': next_arrival}
                resultados_simulacion.append(evento)
                with cancha.request(priority=prioridad(tipo)) as turno:
                    yield turno
                    duracion_ocupacion = random.randint(ocupacion_inf, ocupacion_sup)
                    evento = {'hora': env.now, 'evento': f'Entra {grupo_id}', 'duracion': duracion_ocupacion}
                    resultados_simulacion.append(evento)
                    yield env.timeout(duracion_ocupacion)
                    tiempo_limpieza_ocupado.append(env.now)
                    with limpieza.request() as limpieza_turno:
                        yield limpieza_turno
                        yield env.timeout(tiempo_demora_limpieza)
                iteraciones += 1

        def prioridad(tipo):
            if tipo == 'handball':
                return 2
            return 1

        for _ in range(cantidad_iteraciones):
            # Crear el entorno de simulación
            env = simpy.Environment()

            # Crear los recursos y contenedores para las estadísticas
            cancha = simpy.PriorityResource(env, capacity=1)
            limpieza = simpy.Resource(env, capacity=1)
            tiempos_espera = {'futbol': [], 'handball': [], 'basquet': []}
            tiempo_limpieza_ocupado = []

            # Procesos de llegada
            env.process(llegada_grupo(env, 'futbol', lambda: random.expovariate(1 / media_llegada_futbol), ocupacion_futbol_inf, ocupacion_futbol_sup,
                                      tiempos_espera, tiempo_limpieza_ocupado))
            env.process(llegada_grupo(env, 'basquet', lambda: random.gauss(media_llegada_basquet, desviacion_llegada_basquet),
                                      ocupacion_basquet_inf, ocupacion_basquet_sup, tiempos_espera, tiempo_limpieza_ocupado))
            env.process(llegada_grupo(env, 'handball', lambda: random.gauss(media_llegada_handball, desviacion_llegada_handball),
                                      ocupacion_handball_inf, ocupacion_handball_sup, tiempos_espera, tiempo_limpieza_ocupado))

            # Ejecutar la simulación
            env.run(until=min(tiempo_total, 100000))

            if iteraciones >= 100000:
                break

        return resultados_simulacion

    def mostrar_resultados(self, resultados_simulacion, cantidad_filas, hora_especifica):
        resultados_filtrados = [fila for fila in resultados_simulacion if fila['hora'] >= hora_especifica]
        resultados_mostrados = resultados_filtrados[:cantidad_filas] + [resultados_simulacion[-1]]

        # Mostrar resultados en una nueva ventana
        ventana_resultados = tk.Toplevel(self.root)
        ventana_resultados.title("Resultados de la simulación")

        ttk.Label(ventana_resultados, text="Resultados de la simulación").grid(row=0, column=0, columnspan=4, pady=5)

        headers = ["Hora", "Evento", "Siguiente Evento", "Duración"]
        for col, header in enumerate(headers):
            ttk.Label(ventana_resultados, text=header).grid(row=1, column=col, padx=5, pady=5, sticky=tk.W)

        for row, resultado in enumerate(resultados_mostrados):
            ttk.Label(ventana_resultados, text=str(resultado['hora'])).grid(row=row + 2, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Label(ventana_resultados, text=resultado['evento']).grid(row=row + 2, column=1, padx=5, pady=5, sticky=tk.W)
            ttk.Label(ventana_resultados, text=str(resultado.get('siguiente_evento', ''))).grid(row=row + 2, column=2, padx=5, pady=5, sticky=tk.W)
            ttk.Label(ventana_resultados, text=str(resultado.get('duracion', ''))).grid(row=row + 2, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy).grid(row=row + 3, column=3, pady=5, sticky=tk.E)

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()



