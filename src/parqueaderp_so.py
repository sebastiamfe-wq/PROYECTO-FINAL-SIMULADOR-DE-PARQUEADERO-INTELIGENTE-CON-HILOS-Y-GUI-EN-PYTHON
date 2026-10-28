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


def calc_availability(capacity, occupied):
    """Retorna los espacios disponibles"""
    return capacity - occupied


def calc_occupation_rate(capacity, occupied):
    """Devuelve el porcentaje de ocupación (0 a 100). Si la capacidad es 0, devuelve 0."""
    if capacity == 0:
        return 0
    rate = (occupied / capacity) * 100
    return rate


def calc_occupation_state(rate):
    """Clasifica el porcentaje de ocupacion en: low, medium, high"""
    if rate < 50:
        state = "Low"
    elif rate < 90:
        state = "Medium"
    else:
        state = "High"
    return state


def calc_vehicles_waiting(vehicle_log):
    """Cuenta cuantos vehiculos del registro estan esperando"""
    waiting = 0
    for v in vehicle_log:
        if v["state"] == "waiting":
            waiting += 1
    return waiting


def main():
    """Funcion principal que contiene toda la logica del programa"""
    random.seed(
        SEED
    )  # La semilla fija hace que cada ejecución produzca los mismos resultados.
    occupied_spaces = 0
    vehicle_log = []
    start = time.time()

    for current_vehicle in range(1, TOTAL_VEHICLES + 1):
        time.sleep(random.uniform(MIN_ARRIVAL_TIME, MAX_ARRIVAL_TIME))
        arrival_time = (
            time.time() - start
        )  # La llegada va antes del if: todo vehículo llega, haya espacio o no.
        random_parking_time = random.randint(MIN_PARKING_TIME, MAX_PARKING_TIME)

        if occupied_spaces < MAX_CAPACITY:
            occupied_spaces += 1
            vehicle_status = "parked"
            print(
                f"[{arrival_time:.2f}] Vehicle {current_vehicle} enters | Occupied: {occupied_spaces} | Availability: {calc_availability(MAX_CAPACITY, occupied_spaces)} | Parking time: {random_parking_time}"
            )

        else:
            vehicle_status = "waiting"
            print(
                f"[{arrival_time:.2f}] Vehicle {current_vehicle} doesn't enter, full parking lot | Parking time: {random_parking_time}"
            )

        vehicle_log.append(
            {
                "vehicle_id": current_vehicle,
                "state": vehicle_status,
                "arrival_time": arrival_time,
                "parking_time": random_parking_time,
            }
        )

    print()
    availability_spaces = calc_availability(MAX_CAPACITY, occupied_spaces)
    occupation_rate = calc_occupation_rate(MAX_CAPACITY, occupied_spaces)
    occupation_state = calc_occupation_state(occupation_rate)
    vehicles_waiting = calc_vehicles_waiting(vehicle_log)

    for vehicle in vehicle_log:
        print(f"Vehicle {vehicle['vehicle_id']}: {vehicle['state']}")

    print()
    print(
        f"Capacity: {MAX_CAPACITY} | Occupied: {occupied_spaces} | Availability: {availability_spaces} | Occupation: {occupation_state}({occupation_rate:.1f}%) | Waiting: {vehicles_waiting}"
    )
    print()
    total_simulation_time = time.time() - start
    print(f"Simulation:{total_simulation_time:.2f}")


if __name__ == "__main__":
    main()
