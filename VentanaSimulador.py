import tkinter as tk
from tkinter import ttk
import random
import heapq

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

        # Inicializar el polideportivo y la fila de eventos
        polideportivo = Polideportivo()
        fila = Fila(0, polideportivo)

        # Agregar evento de inicialización
        fila.agregar_evento(0, lambda: None, "Inicialización")

        # Generar eventos de llegada
        def llegada_equipo(tipo):
            def evento():
                polideportivo.agregar_equipo(tipo)
                if polideportivo.estado == "Cancha Libre":
                    fila.agregar_evento(fila.reloj, ocupar_cancha, "Ocupar Cancha")
            if tipo == 'futbol':
                return evento, "Llegada de Equipo Futbol"
            elif tipo == 'basquet':
                return evento, "Llegada de Equipo BasketBall"
            elif tipo == 'handball':
                return evento, "Llegada de Equipo HandBall"

        def ocupar_cancha():
            tipo = polideportivo.tipo_siguiente_equipo()
            if tipo == 'basquet':
                polideportivo.ocupar(basquet=True)
                tiempo_ocupacion = random.uniform(fin_ocupacion_basquet_inf, fin_ocupacion_basquet_sup)
                fila.agregar_evento(fila.reloj + tiempo_ocupacion, liberar_cancha, "Fin de ocupacion de cancha BasketBall")
            elif tipo == 'futbol/handball':
                polideportivo.ocupar()
                if random.choice([True, False]):  # Randomly choose between fútbol and handball
                    tiempo_ocupacion = random.uniform(fin_ocupacion_futbol_inf, fin_ocupacion_futbol_sup)
                    fila.agregar_evento(fila.reloj + tiempo_ocupacion, liberar_cancha, "Fin de ocupacion de cancha Futbol")
                else:
                    tiempo_ocupacion = random.uniform(fin_ocupacion_handball_inf, fin_ocupacion_handball_sup)
                    fila.agregar_evento(fila.reloj + tiempo_ocupacion, liberar_cancha, "Fin de ocupacion de cancha HandBall")

        def liberar_cancha():
            polideportivo.liberar()
            fila.agregar_evento(fila.reloj, limpieza_cancha, "Limpieza Cancha")

        def limpieza_cancha():
            fila.agregar_evento(fila.reloj + tiempo_demora_limpieza, finalizar_limpieza, "Fin de limpieza de cancha")

        def finalizar_limpieza():
            polideportivo.liberar()
            if polideportivo.hay_equipos_en_espera():
                fila.agregar_evento(fila.reloj, ocupar_cancha, "Ocupar Cancha")

        # Agregar eventos iniciales
        evento, nombre_evento = llegada_equipo('futbol')
        fila.agregar_evento(random.expovariate(1.0 / media_llegada_futbol), evento, nombre_evento)

        evento, nombre_evento = llegada_equipo('basquet')
        fila.agregar_evento(random.uniform(intervalo_llegada_basquet_inf, intervalo_llegada_basquet_sup), evento, nombre_evento)

        evento, nombre_evento = llegada_equipo('handball')
        fila.agregar_evento(random.uniform(intervalo_llegada_handball_inf, intervalo_llegada_handball_sup), evento, nombre_evento)

        # Ejecutar la simulación
        while fila.reloj < tiempo_total and fila.event_queue:
            fila.procesar_evento()

        # Mostrar resultados
        self.mostrar_resultados(fila.event_log, cantidad_filas, hora_especifica)

    def mostrar_resultados(self, eventos, cantidad_filas, hora_especifica):
        print(f"Mostrando {cantidad_filas} filas de eventos a partir de la hora {hora_especifica}:")

        # Filtrar los eventos a partir de la hora específica
        eventos_filtrados = [evento for evento in eventos if evento[0] >= hora_especifica]

        # Mostrar solo la cantidad de filas solicitada
        for evento in eventos_filtrados[:cantidad_filas]:
            tiempo_truncado = self.truncar(evento[0])
            print(f"{tiempo_truncado:.2f}: {evento[1]}")

class Polideportivo:
    def __init__(self):
        self.nombre = "Polideportivo General Paz"
        self.estado = "Cancha Libre"
        self.colaFyH = 0
        self.colaB = 0
        self.cola = []

    def agregar_equipo(self, tipo):
        if tipo == 'basquet':
            self.colaB += 1
        else:
            self.colaFyH += 1
        self.cola.append(tipo)

    def tipo_siguiente_equipo(self):
        if self.cola:
            return self.cola.pop(0)
        return None

    def ocupar(self, basquet=False):
        self.estado = "Cancha Ocupada"
        if basquet:
            self.colaB -= 1
        else:
            self.colaFyH -= 1

    def liberar(self):
        self.estado = "Cancha Libre"

    def hay_equipos_en_espera(self):
        return self.colaFyH > 0 or self.colaB > 0

class Fila:
    def __init__(self, reloj, polideportivo):
        self.reloj = reloj
        self.polideportivo = polideportivo
        self.event_queue = []
        self.event_log = []

    def agregar_evento(self, tiempo, evento, nombre_evento):
        heapq.heappush(self.event_queue, (tiempo, evento, nombre_evento))

    def procesar_evento(self):
        tiempo, evento, nombre_evento = heapq.heappop(self.event_queue)
        self.reloj = tiempo
        evento()
        self.event_log.append((tiempo, nombre_evento))

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()
