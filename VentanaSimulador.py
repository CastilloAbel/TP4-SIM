import tkinter as tk
from tkinter import ttk

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
            "Intervalo inferior de llegada de equipo de básquet:", "Intervalo superior de llegada de equipo de básquet:",
            "Intervalo inferior de llegada de equipo de handball:", "Intervalo superior de llegada de equipo de handball:",
            "Intervalo inferior de ocupación de equipo de fútbol:", "Intervalo superior de ocupación de equipo de fútbol:",
            "Intervalo inferior de ocupación de equipo de básquet:", "Intervalo superior de ocupación de equipo de básquet:",
            "Intervalo inferior de ocupación de equipo de handball:", "Intervalo superior de ocupación de equipo de handball:",
             "Cantidad de equipos en cola máxima:",
            "Cantidad de filas a mostrar (I):", "Hora específica a mostrar (J):"
        ]
        
        self.entries = []
        for i, text in enumerate(labels_text):
            ttk.Label(self.frame, text=text).grid(column=0, row=i, sticky=tk.W)
            entry = ttk.Entry(self.frame)
            entry.grid(column=1, row=i, sticky=(tk.W, tk.E))
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
        tiempo_demora_limpieza = int(params[1])
        media_llegada_futbol = float(params[2])
        intervalo_llegada_basquet_inf = int(params[3])
        intervalo_llegada_basquet_sup = int(params[4])
        intervalo_llegada_handball_inf = int(params[5])
        intervalo_llegada_handball_sup = int(params[6])
        ocupacion_futbol_inf = int(params[7])
        ocupacion_futbol_sup = int(params[8])
        ocupacion_basquet_inf = int(params[9])
        ocupacion_basquet_sup = int(params[10])
        ocupacion_handball_inf = int(params[11])
        ocupacion_handball_sup = int(params[12])
        cantidad_equipos_max = int(params[13])
        cantidad_filas = int(params[14])
        hora_especifica = int(params[15])

        # Aquí puedes llamar a tu función de simulación con los parámetros obtenidos
        # simulate(tiempo_total, tiempo_demora_limpieza, media_llegada_futbol, ...)
        print(f"Simulación iniciada con parámetros: {params}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaSimulador(root)
    root.mainloop()
