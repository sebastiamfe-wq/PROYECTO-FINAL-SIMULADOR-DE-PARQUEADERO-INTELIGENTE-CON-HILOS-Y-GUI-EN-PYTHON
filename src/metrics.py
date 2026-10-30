import csv


def calc_average_wait(events):
    """Devuelve el tiempo promedio que esperaron los vehículos que lograron entrar."""
    arrivals = {}  # vehicle_id -> momento en que llegó
    waits = []  # segundos que esperó cada vehículo que entró
    for event in events:
        if event["event"] == "arrives":
            arrivals[event["vehicle_id"]] = event["time"]
        elif event["event"] == "enters":
            waits.append(event["time"] - arrivals[event["vehicle_id"]])

    if len(waits) == 0:
        return 0
    return sum(waits) / len(waits)

def calc_utilization(events, capacity, now):
    """Devuelve el porcentaje de la capacidad que estuvo ocupada entre 0 y now.
    Suma cuántos segundos estuvo ocupado cada espacio y lo compara con el total
    disponible: capacidad por el  tiempo transcurrido.
    """
    if capacity == 0 or now == 0:
        return 0

    entries = {}  # vehicle_id -> momento en que entró (de los que siguen adentro)
    occupied_time = 0
    for event in events:
        if event["event"] == "enters":
            entries[event["vehicle_id"]] = event["time"]
        elif event["event"] == "leaves":
            # pop() saca al vehículo del diccionario y devuelve su momento de entrada.
            occupied_time += event["time"] - entries.pop(event["vehicle_id"])
    # Los que siguen estacionados cuentan hasta este momento.
    for entry_time in entries.values():
        occupied_time += now - entry_time
    return occupied_time / (capacity * now) * 100

def save_events_csv(events, path):
    """Guarda todos los eventos de la simulación en un archivo CSV."""
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["time", "vehicle_id", "event"])
        for event in events:
            writer.writerow(
                [round(event["time"], 3), event["vehicle_id"], event["event"]]
            )