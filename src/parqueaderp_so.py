"""SIMULADOR DE PARQUEADERO INTELIGENTE CON HILOS Y GUI EN PYTHON
Proyecto final -> Arquitectura de Computadores y Sistemas Operativos
"""

import random
import time

MAX_CAPACITY = 3
TOTAL_VEHICLES = 5
SEED = 333
MIN_ARRIVAL_TIME = 0.2  # segundos
MAX_ARRIVAL_TIME = 1  # segundos
MIN_PARKING_TIME = 2  # segundos
MAX_PARKING_TIME = 6  # segundos


def calc_occupation_state(rate):
    """Clasifica el porcentaje de ocupacion en: low, medium, high"""
    if rate < 50:
        state = "Low"
    elif rate < 90:
        state = "Medium"
    else:
        state = "High"
    return state


class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.occupied_spaces = 0
        self.vehicle_log = []

    def calc_availability(self):
        """Retorna los espacios disponibles"""
        return self.capacity - self.occupied_spaces

    def calc_occupation_rate(self):
        """Devuelve el porcentaje de ocupación (0 a 100). Si la capacidad es 0, devuelve 0."""
        if self.capacity == 0:
            return 0
        rate = (self.occupied_spaces / self.capacity) * 100
        return rate

    def calc_vehicles_waiting(self):
        """Cuenta cuantos vehiculos del registro estan esperando"""
        waiting = 0
        for v in self.vehicle_log:
            if v["state"] == "waiting":
                waiting += 1
        return waiting

    def parking_vehicle(self):
        if self.occupied_spaces < self.capacity:
            self.occupied_spaces += 1


def main():
    """Funcion principal que contiene toda la logica del programa"""
    parking_lot = ParkingLot(MAX_CAPACITY)
    print(parking_lot.capacity)
    random.seed(
        SEED
    )  # La semilla fija hace que cada ejecución produzca los mismos resultados.
    start = time.time()
    for current_vehicle in range(1, TOTAL_VEHICLES + 1):
        time.sleep(random.uniform(MIN_ARRIVAL_TIME, MAX_ARRIVAL_TIME))
        arrival_time = (
            time.time() - start
        )  # La llegada va antes del if: todo vehículo llega, haya espacio o no.
        random_parking_time = random.randint(MIN_PARKING_TIME, MAX_PARKING_TIME)
        if  parking_lot.occupied_spaces < parking_lot.capacity:
            parking_lot.parking_vehicle()
            vehicle_status = "parked"
            print(
                f"[{arrival_time:.2f}] Vehicle {current_vehicle} enters | Occupied: {parking_lot.occupied_spaces} | Availability: {parking_lot.calc_availability()} | Parking time: {random_parking_time}"
            )
        else:
            vehicle_status = "waiting"
            print(
                f"[{arrival_time:.2f}] Vehicle {current_vehicle} doesn't enter, full parking lot | Parking time: {random_parking_time}"
            )
        parking_lot.vehicle_log.append(
            {
                "vehicle_id": current_vehicle,
                "state": vehicle_status,
                "arrival_time": arrival_time,
                "parking_time": random_parking_time,
            }
        )
    print()
    rate = parking_lot.calc_occupation_rate()
    state = calc_occupation_state(rate)
    for vehicle in parking_lot.vehicle_log:
        print(f"Vehicle {vehicle['vehicle_id']}: {vehicle['state']}")
    print()
    print(
        f"Capacity: {MAX_CAPACITY} | Occupied: {parking_lot.occupied_spaces} | Availability: {parking_lot.calc_availability()} | Occupation: {state}({rate:.1f}%) | Waiting: {parking_lot.calc_vehicles_waiting()}",
        end="\n\n",
    )
    total_simulation_time = time.time() - start
    print(f"Simulation:{total_simulation_time:.2f}")


if __name__ == "__main__":
    main()