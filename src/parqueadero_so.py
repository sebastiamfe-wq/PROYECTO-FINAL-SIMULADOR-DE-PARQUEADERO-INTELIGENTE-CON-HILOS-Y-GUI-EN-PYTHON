import random
import time
import threading

MAX_CAPACITY = 3
TOTAL_VEHICLES = 5
SEED = 33
MIN_ARRIVAL_TIME = 0.1  # segundos
MAX_ARRIVAL_TIME = 8  # segundos
MIN_PARKING_TIME = 2  # segundos
MAX_PARKING_TIME = 6  # segundos


def calc_random_number(min_a_t, max_a_t, min_p_t, max_p_t):
    arrival_t = random.uniform(min_a_t, max_a_t)
    parking_t = random.randint(min_p_t, max_p_t)
    return arrival_t, parking_t


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
    """representa un parqueadero con su capacidad, sus espacios ocupados y su registro de vehículos."""

    def __init__(self, capacity):
        """Crea un parqueadero y su registro vacios y se le asigna la capacidad por parametro"""
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

    def park_vehicle(self, vehicle_id, arrival_time, parking_time):
        """Decide si el vehiculo entra o no y lo registra"""
        if self.occupied_spaces < self.capacity:
            self.occupied_spaces += 1
            vehicle_status = "parked"
        else:
            vehicle_status = "waiting"
        self.vehicle_log.append(
            {
                "vehicle_id": vehicle_id,
                "state": vehicle_status,
                "arrival_time": arrival_time,
                "parking_time": parking_time,
            }
        )
        return vehicle_status == "parked"


def main():
    """Ejecuta la simulacion y muestra los resultados"""
    parking_lot = ParkingLot(MAX_CAPACITY)
    random.seed(
        SEED
    )  # La semilla fija hace que cada ejecución produzca los mismos resultados.
    start = time.time()
    for current_vehicle in range(1, TOTAL_VEHICLES + 1):
        # Cualquier vehiculo llega antes de intentar estacionar, haya espacio o no.
        arrival_delay, parking_time = calc_random_number(
            MIN_ARRIVAL_TIME, MAX_ARRIVAL_TIME, MIN_PARKING_TIME, MAX_PARKING_TIME
        )
        time.sleep(arrival_delay)
        arrival_time = time.time() - start
        entered = parking_lot.park_vehicle(current_vehicle, arrival_time, parking_time)
        if entered:
            print(
                f"[{arrival_time:.2f}] Vehicle {current_vehicle} enters | Occupied: {parking_lot.occupied_spaces} | Availability: {parking_lot.calc_availability()} | Parking time: {parking_time}"
            )
        else:
            print(
                f"[{arrival_time:.2f}] Vehicle {current_vehicle} doesn't enter, full parking lot | Parking time: {parking_time}"
            )

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
