import random
import time


def calc_random_number(min_a_t, max_a_t, min_p_t, max_p_t):
    arrival_t = random.uniform(min_a_t, max_a_t)
    parking_t = random.randint(min_p_t, max_p_t)
    return arrival_t, parking_t


def vehicle_lifecycle(parking_lot, vehicle_id, arrival_delay, parking_time, start):
    """Simula la vida de un vehiculo o hilo llega estaciona un tiempo y sale."""
    time.sleep(arrival_delay)
    arrival_time = time.time() - start

    print(
        f"[{arrival_time:.2f}] Vehicle {vehicle_id} arrives | Parking time: {parking_time}"
    )

    parking_lot.park_vehicle(vehicle_id, arrival_time, parking_time)
    entry_time = time.time() - start
    waited = entry_time - arrival_time
    print(
        f"[{entry_time:.2f}] Vehicle {vehicle_id} enters | Occupied: {parking_lot.occupied_spaces} | Availability: {parking_lot.calc_availability()} | Waited: {waited:.2f}s"
    )

    time.sleep(parking_time)

    parking_lot.pick_up_vehicle(vehicle_id)
    departure_time = time.time() - start
    print(
        f"[{departure_time:.2f}] Vehicle {vehicle_id} leaves | Occupied: {parking_lot.occupied_spaces} | Availability: {parking_lot.calc_availability()}"
    )