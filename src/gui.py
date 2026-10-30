"""Ventana del simulador: muestra el parqueadero y controla la simulación."""

import queue
import random
import threading
import time
import tkinter as tk
from tkinter import ttk

from config import (
    MAX_ARRIVAL_TIME,
    MAX_CAPACITY,
    MAX_PARKING_TIME,
    MIN_ARRIVAL_TIME,
    MIN_PARKING_TIME,
    SEED,
    TOTAL_VEHICLES,
)
from metrics import calc_average_wait, calc_utilization, save_events_csv
from parking import ParkingLot, calc_occupation_state
from simulation import calc_random_number, vehicle_lifecycle

REFRESH_MS = 100  # cada cuántos milisegundos se actualiza la ventana
CSV_PATH = "events.csv"  # archivo donde se guardan los eventos al terminar

# Textos que se muestran en pantalla para cada estado y cada evento.
STATE_TEXT = {"waiting": "esperando", "parked": "estacionado", "left": "salió"}
EVENT_TEXT = {"arrives": "llega", "enters": "entra", "leaves": "sale"}


class ParkingApp:
    """Ventana del simulador de parqueadero."""

    def __init__(self, root):
        self.root = root
        self.parking_lot = ParkingLot(MAX_CAPACITY)
        # Buzón donde los hilos de los vehículos dejan sus eventos.
        self.events = queue.Queue()
        self.event_log = []
        self.threads = []
        self.start_time = None
        self.finished = False

        root.title("Simulador de parqueadero")

        # Fila 1: el estado del parqueadero 
        info_frame = ttk.Frame(root)
        info_frame.pack(padx=10, pady=(10, 2))

        self.occupied_label = ttk.Label(info_frame)
        self.occupied_label.pack(side="left", padx=10)
        self.available_label = ttk.Label(info_frame)
        self.available_label.pack(side="left", padx=10)
        self.waiting_label = ttk.Label(info_frame)
        self.waiting_label.pack(side="left", padx=10)
        self.occupation_label = ttk.Label(info_frame)
        self.occupation_label.pack(side="left", padx=10)

        # Fila 2: las métricas
        metrics_frame = ttk.Frame(root)
        metrics_frame.pack(padx=10, pady=(2, 10))

        self.time_label = ttk.Label(metrics_frame)
        self.time_label.pack(side="left", padx=10)
        self.wait_label = ttk.Label(metrics_frame)
        self.wait_label.pack(side="left", padx=10)
        self.utilization_label = ttk.Label(metrics_frame)
        self.utilization_label.pack(side="left", padx=10)

        # Fila 3: la lista de vehículos y el registro de eventos
        lists_frame = ttk.Frame(root)
        lists_frame.pack(padx=10, pady=5)

        vehicles_box = ttk.LabelFrame(lists_frame, text="Vehículos")
        vehicles_box.pack(side="left", padx=5)
        self.vehicle_list = tk.Listbox(vehicles_box, width=30, height=15)
        self.vehicle_list.pack(padx=5, pady=5)

        events_box = ttk.LabelFrame(lists_frame, text="Eventos")
        events_box.pack(side="left", padx=5)
        self.event_list = tk.Listbox(events_box, width=34, height=15)
        self.event_list.pack(padx=5, pady=5)

        # Fila 4: el botón y el estado de la simulación
        self.start_button = ttk.Button(
            root, text="Iniciar simulación", command=self.start_simulation
        )
        self.start_button.pack(pady=(10, 5))

        self.status_label = ttk.Label(root, text="Lista para iniciar.")
        self.status_label.pack(pady=(5, 10))

        # Primera actualización. Desde ahí, refresh se vuelve a programar sola.
        self.refresh()

    def start_simulation(self):
        """Crea un hilo por vehículo y los pone a correr, sin esperar a que terminen."""
        # Evita que la simulación se inicie dos veces.
        self.start_button.config(state="disabled")
        self.status_label.config(text="Simulación en curso.")

        # La semilla fija hace que cada ejecución produzca los mismos resultados.
        random.seed(SEED)
        self.start_time = time.time()

        for vehicle_id in range(1, TOTAL_VEHICLES + 1):
            arrival_delay, parking_time = calc_random_number(
                MIN_ARRIVAL_TIME, MAX_ARRIVAL_TIME, MIN_PARKING_TIME, MAX_PARKING_TIME
            )
            thread = threading.Thread(
                target=vehicle_lifecycle,
                args=(
                    self.parking_lot,
                    vehicle_id,
                    arrival_delay,
                    parking_time,
                    self.start_time,
                    self.events,
                ),
                daemon=True,
            )
            thread.start()
            self.threads.append(thread)
        # No hay join(): si la ventana esperara a los hilos, se congelaría.

    def any_vehicle_alive(self):
        """Devuelve True si al menos un hilo de vehículo sigue corriendo."""
        for thread in self.threads:
            if thread.is_alive():
                return True
        return False

    def elapsed_time(self):
        """Segundos de simulación: hasta ahora, o hasta el último evento si terminó."""
        if self.start_time is None:
            return 0
        if self.finished:
            if len(self.event_log) == 0:
                return 0
            return self.event_log[-1]["time"]
        return time.time() - self.start_time

    def finish_simulation(self):
        """Marca la simulación como terminada y guarda los eventos en el CSV."""
        self.finished = True
        save_events_csv(self.event_log, CSV_PATH)
        self.status_label.config(
            text=f"Simulación terminada. Eventos guardados en {CSV_PATH}."
        )

    def refresh(self):
        """Lee los eventos nuevos y redibuja la ventana. Se repite cada REFRESH_MS."""
        # 1. ¿Ya terminaron todos los vehículos? Se pregunta ANTES de vaciar el
        #    buzón: si todos terminaron, sus últimos eventos ya están en él.
        all_done = (
            self.start_time is not None
            and not self.finished
            and not self.any_vehicle_alive()
        )

        # 2. Vaciar el buzón: guardar cada evento y mostrarlo en el registro.
        while not self.events.empty():
            event = self.events.get()
            self.event_log.append(event)
            text = EVENT_TEXT[event["event"]]
            self.event_list.insert(
                tk.END, f"[{event['time']:.2f}] Vehículo {event['vehicle_id']} {text}"
            )
            # Desplazar la lista para que siempre se vea el último evento.
            self.event_list.see(tk.END)

        if all_done:
            self.finish_simulation()

        # 3. Actualizar las etiquetas con los datos actuales del parqueadero.
        parking_lot = self.parking_lot
        rate = parking_lot.calc_occupation_rate()
        self.occupied_label.config(
            text=f"Ocupados: {parking_lot.occupied_spaces} / {parking_lot.capacity}"
        )
        self.available_label.config(
            text=f"Disponibles: {parking_lot.calc_availability()}"
        )
        self.waiting_label.config(
            text=f"Esperando: {parking_lot.calc_vehicles_waiting()}"
        )
        self.occupation_label.config(
            text=f"Ocupación: {calc_occupation_state(rate)} ({rate:.1f}%)"
        )

        # 4. Actualizar las métricas.
        elapsed = self.elapsed_time()
        average_wait = calc_average_wait(self.event_log)
        utilization = calc_utilization(self.event_log, parking_lot.capacity, elapsed)
        self.time_label.config(text=f"Tiempo: {elapsed:.2f} s")
        self.wait_label.config(text=f"Espera promedio: {average_wait:.2f} s")
        self.utilization_label.config(text=f"Utilización: {utilization:.1f}%")

        # 5. Redibujar la lista de vehículos desde una copia del registro.
        self.vehicle_list.delete(0, tk.END)
        for vehicle in parking_lot.get_vehicles():
            state = STATE_TEXT[vehicle["state"]]
            self.vehicle_list.insert(
                tk.END, f"Vehículo {vehicle['vehicle_id']}: {state}"
            )

        # 6. Programar la próxima actualización, sin bloquear la ventana.
        self.root.after(REFRESH_MS, self.refresh)
