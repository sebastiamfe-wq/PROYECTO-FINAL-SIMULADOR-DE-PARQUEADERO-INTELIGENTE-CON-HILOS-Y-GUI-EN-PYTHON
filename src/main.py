import threading
import time
import random

from config import (
    MAX_ARRIVAL_TIME,
    MAX_CAPACITY,
    MAX_PARKING_TIME,
    MIN_ARRIVAL_TIME,
    MIN_PARKING_TIME,
    SEED,
    TOTAL_VEHICLES,
)
from parking import ParkingLot, calc_occupation_state
from simulation import calc_random_number, vehicle_lifecycle


def main():
    """Ejecuta la simulacion y muestra los resultados"""
    start = time.time()
    parking_lot = ParkingLot(MAX_CAPACITY)
    # La semilla fija hace que cada ejecución produzca los mismos resultados.
    random.seed(SEED)
    threads = []

    for current_vehicle in range(1, TOTAL_VEHICLES + 1):
        arrival_delay, parking_time = calc_random_number(
            MIN_ARRIVAL_TIME, MAX_ARRIVAL_TIME, MIN_PARKING_TIME, MAX_PARKING_TIME
        )
        thread = threading.Thread(
            target=vehicle_lifecycle,
            args=(parking_lot, current_vehicle, arrival_delay, parking_time, start),
        )
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print()
    for vehicle in parking_lot.vehicle_log:
        print(f"Vehicle {vehicle['vehicle_id']}: {vehicle['state']}")
    print()

    occupation_rate = parking_lot.calc_occupation_rate()
    occupation_state = calc_occupation_state(occupation_rate)
    print(
        f"Capacity: {parking_lot.capacity} | Occupied: {parking_lot.occupied_spaces} | Availability: {parking_lot.calc_availability()} | Occupation: {occupation_state}({occupation_rate:.1f}%) | Waiting: {parking_lot.calc_vehicles_waiting()}",
        end="\n\n",
    )
    total_simulation_time = time.time() - start
    print(f"Simulation:{total_simulation_time:.2f}")


if __name__ == "__main__":
    main()
