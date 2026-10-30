import threading


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
        self.spaces = threading.Semaphore(capacity)
        self.lock = threading.Lock()
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
        with self.lock:
            for v in self.vehicle_log:
                if v["state"] == "waiting":
                    waiting += 1
        return waiting

    def get_vehicles(self):
        with self.lock:
            return list(self.vehicle_log)

    def park_vehicle(self, vehicle_id, arrival_time, parking_time):
        """Decide si el vehiculo entra o no y lo registra"""
        vehicle = {
            "vehicle_id": vehicle_id,
            "state": "waiting",
            "arrival_time": arrival_time,
            "parking_time": parking_time,
        }
        with self.lock:
            self.vehicle_log.append(vehicle)

        self.spaces.acquire()

        with self.lock:
            self.occupied_spaces += 1
            vehicle["state"] = "parked"

    def pick_up_vehicle(self, vehicle_id):
        with self.lock:
            for v in self.vehicle_log:
                if v["vehicle_id"] == vehicle_id and v["state"] == "parked":
                    self.occupied_spaces -= 1
                    v["state"] = "left"
                    self.spaces.release()
                    break