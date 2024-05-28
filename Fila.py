import heapq
import random

class Fila:
    def __init__(self, tiempo_total, tiempo_demora_limpieza, media_llegada_futbol, 
                 intervalo_llegada_basquet, intervalo_llegada_handball, 
                 ocupacion_futbol, ocupacion_basquet, ocupacion_handball):
        self.tiempo_total = tiempo_total
        self.tiempo_demora_limpieza = tiempo_demora_limpieza
        self.media_llegada_futbol = media_llegada_futbol
        self.intervalo_llegada_basquet = intervalo_llegada_basquet
        self.intervalo_llegada_handball = intervalo_llegada_handball
        self.ocupacion_futbol = ocupacion_futbol
        self.ocupacion_basquet = ocupacion_basquet
        self.ocupacion_handball = ocupacion_handball

        self.tiempo_actual = 0
        self.eventos = []
        self.cola_futbol_handball = []
        self.cola_basquet = []
        self.ocupado_futbol = False
        self.ocupado_handball = False
        self.ocupado_basquet = False

        self.generar_eventos_iniciales()

    def generar_eventos_iniciales(self):
        tiempo_llegada_futbol = random.expovariate(1.0 / self.media_llegada_futbol)
        heapq.heappush(self.eventos, (tiempo_llegada_futbol, 'llegada_futbol'))

        tiempo_llegada_basquet = random.uniform(*self.intervalo_llegada_basquet)
        heapq.heappush(self.eventos, (tiempo_llegada_basquet, 'llegada_basquet'))

        tiempo_llegada_handball = random.uniform(*self.intervalo_llegada_handball)
        heapq.heappush(self.eventos, (tiempo_llegada_handball, 'llegada_handball'))

    def procesar_eventos(self):
        while self.tiempo_actual < self.tiempo_total and self.eventos:
            tiempo_evento, tipo_evento = heapq.heappop(self.eventos)
            self.tiempo_actual = tiempo_evento

            if tipo_evento == 'llegada_futbol':
                self.procesar_llegada('futbol')
            elif tipo_evento == 'llegada_basquet':
                self.procesar_llegada('basquet')
            elif tipo_evento == 'llegada_handball':
                self.procesar_llegada('handball')
            elif tipo_evento == 'ocupacion_futbol':
                self.procesar_ocupacion('futbol')
            elif tipo_evento == 'ocupacion_basquet':
                self.procesar_ocupacion('basquet')
            elif tipo_evento == 'ocupacion_handball':
                self.procesar_ocupacion('handball')
            elif tipo_evento == 'limpieza_cancha':
                self.procesar_limpieza()

    def procesar_llegada(self, equipo):
        if equipo == 'futbol':
            self.cola_futbol_handball.append(('futbol', self.tiempo_actual))
            tiempo_llegada_futbol = self.tiempo_actual + random.expovariate(1.0 / self.media_llegada_futbol)
            heapq.heappush(self.eventos, (tiempo_llegada_futbol, 'llegada_futbol'))
        elif equipo == 'basquet':
            self.cola_basquet.append(('basquet', self.tiempo_actual))
            tiempo_llegada_basquet = self.tiempo_actual + random.uniform(*self.intervalo_llegada_basquet)
            heapq.heappush(self.eventos, (tiempo_llegada_basquet, 'llegada_basquet'))
        elif equipo == 'handball':
            self.cola_futbol_handball.append(('handball', self.tiempo_actual))
            tiempo_llegada_handball = self.tiempo_actual + random.uniform(*self.intervalo_llegada_handball)
            heapq.heappush(self.eventos, (tiempo_llegada_handball, 'llegada_handball'))

        self.verificar_ocupacion()

    def verificar_ocupacion(self):
        if self.cola_futbol_handball and not self.ocupado_futbol and not self.ocupado_handball:
            equipo, tiempo_llegada = self.cola_futbol_handball.pop(0)
            if equipo == 'futbol':
                self.ocupado_futbol = True
                tiempo_ocupacion = random.uniform(*self.ocupacion_futbol)
                tiempo_fin_ocupacion = self.tiempo_actual + tiempo_ocupacion
                heapq.heappush(self.eventos, (tiempo_fin_ocupacion, 'ocupacion_futbol'))
            elif equipo == 'handball':
                self.ocupado_handball = True
                tiempo_ocupacion = random.uniform(*self.ocupacion_handball)
                tiempo_fin_ocupacion = self.tiempo_actual + tiempo_ocupacion
                heapq.heappush(self.eventos, (tiempo_fin_ocupacion, 'ocupacion_handball'))

        if self.cola_basquet and not self.ocupado_basquet:
            equipo, tiempo_llegada = self.cola_basquet.pop(0)
            self.ocupado_basquet = True
            tiempo_ocupacion = random.uniform(*self.ocupacion_basquet)
            tiempo_fin_ocupacion = self.tiempo_actual + tiempo_ocupacion
            heapq.heappush(self.eventos, (tiempo_fin_ocupacion, 'ocupacion_basquet'))

    def procesar_ocupacion(self, equipo):
        if equipo == 'futbol':
            self.ocupado_futbol = False
        elif equipo == 'handball':
            self.ocupado_handball = False
        elif equipo == 'basquet':
            self.ocupado_basquet = False

        tiempo_limpieza = self.tiempo_actual + self.tiempo_demora_limpieza
        heapq.heappush(self.eventos, (tiempo_limpieza, 'limpieza_cancha'))

        print(f"Fin de ocupación de {equipo} a tiempo {self.tiempo_actual}, limpieza hasta {tiempo_limpieza}")

        self.verificar_ocupacion()

    def procesar_limpieza(self):
        print(f"Limpieza completada a tiempo {self.tiempo_actual}")