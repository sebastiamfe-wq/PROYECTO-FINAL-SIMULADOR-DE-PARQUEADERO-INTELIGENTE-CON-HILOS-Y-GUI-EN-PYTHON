import random
import time


def calc_random_number(min_a_t, max_a_t, min_p_t, max_p_t):
    arrival_t = random.uniform(min_a_t, max_a_t)
    parking_t = random.randint(min_p_t, max_p_t)
    return arrival_t, parking_t


def vehicle_lifecycle(parking_lot, vehicle_id, arrival_delay, parking_time, start, events):
    """Simula la vida de un vehiculo o hilo llega estaciona un tiempo y sale."""
    time.sleep(arrival_delay)
    arrival_time = time.time() - start

    events.put({"time": arrival_time, "vehicle_id": vehicle_id, "event": "arrives"})

    parking_lot.park_vehicle(vehicle_id, arrival_time, parking_time)
    entry_time = time.time() - start
    events.put({"time": entry_time, "vehicle_id": vehicle_id, "event": "enters"})

    time.sleep(parking_time)

    parking_lot.pick_up_vehicle(vehicle_id)
    departure_time = time.time() - start
    events.put({"time": departure_time, "vehicle_id": vehicle_id, "event": "leaves"})