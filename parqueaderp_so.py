#SIMULADOR DE PARQUEADERO INTELIGENTE CON HILOS Y GUI EN PYTHON
#Proyecto final -> Arquitectura de Computadores y Sistemas Operativos

import threading #Permite que corran al mismo tiempo multiples hilos(carros).
import time #Permite utilizar funciones relacionadas al tiempo, medir la duracion de procesos o detenerlos durante una cantidad de segundos entre otras funciones.
import queue #Permite conectar la logica con la interfaz grafica(GUI).
import random #Permite generar eventos aleatorios desde numeros aleatorios hasta seleccionar elementos al azar o simular probabilidades.
import csv #Permite leer y escribir datos en forma de tabla, como generar un archivo .csv o leerlo.
import os #Permite a nuestro codigo interactuar con el sistema operativo, por ejemplo agregar un archivo .csv a nuestra carpeta de proyecto.
import tkinter as tk #Permite crear interfazes graficas de usuario(GUI) y cada vez que lo necesite no es necesario escribir tkinter sino solamente tk.
from tkinter import ttk #Permite separar las logica de un componente de su diseño visual gracias al modulo (ttk).

MAX_CAPACITY = 3 #Variable que se le asigna la capacidad que va a tener el parqueadero.
TOTAL_VEHICLES = 5 #Variable global que simula el total de vehiculos que van a entrar al parqueadero.
SEED = 333
MIN_ARRIVAL_TIME = 0.2
MAX_ARRIVAL_TIME = 1
MIN_PARKING_TIME = 2
MAX_PARKING_TIME = 6

random.seed(SEED)

def calc_availability(capacity, occupied):
    return capacity - occupied

def calc_occupation_rate(capacity, occupied):
    if capacity == 0:
        return 0
    rate = (occupied / capacity) * 100
    return rate

def calc_occupation_state(rate):
    if rate < 50:
        state = "Low"
    elif rate < 90:
        state = "Medium"
    else:
        state = "High"
    return state

def calc_vehicles_waiting(vehicle_log):
    waiting = 0
    for v in vehicle_log:
        if v["state"] == "waiting":
            waiting += 1
    return waiting


occupied_spaces = 0 #Representa los espacios que se van a ocupar, por eso se inicializa en cero. 
vehicle_log = [] #Es donde esta la lista de diccionarios, es decir el registro de cada vehiculo.

start = time.time()

#===========
#El ciclo cumple la funcion de permitir que un vehiculo entre o no.
#===========
for current_vehicle in range(1,TOTAL_VEHICLES + 1):
    time.sleep(random.uniform(MIN_ARRIVAL_TIME, MAX_ARRIVAL_TIME))
    arrival_time = time.time() - start
    random_parking_time = random.randint(MIN_PARKING_TIME, MAX_PARKING_TIME)

    if occupied_spaces < MAX_CAPACITY: #Si entra, ocupa un espacio y registra el vehiculo como estacionado.
        occupied_spaces += 1
        vehicle_status = "parked"
        print(f"[{arrival_time:.4f}] Vehicle {current_vehicle} enters | Occupied: {occupied_spaces} | Availability: {calc_availability(MAX_CAPACITY, occupied_spaces)} | Parking time: {random_parking_time}")

    else: #Si no entra, solamente registra el vehiculo como waiting a un espacio.
        vehicle_status = "waiting"
        print(f"[{arrival_time:.4f}] Vehicle {current_vehicle} doesn't enter, full parking lot | Parking time: {random_parking_time}")

    vehicle_log.append({"vehicle_id": current_vehicle, "state": vehicle_status, "arrival_time": arrival_time, "parking_time": random_parking_time})

print()
availability_spaces = calc_availability(MAX_CAPACITY, occupied_spaces) #Guarda los espacios diponibles que la funcion de calculo le da.
occupation_rate = calc_occupation_rate(MAX_CAPACITY, occupied_spaces) #Esta funcione guarda lo que retorna la funcion de ===porcentaje=== de ocuacion.
occupation_state = calc_occupation_state(occupation_rate) #Esta funcione guarda lo que retorna la funcion de ==estado== de ocuacion.
vehicles_waiting = calc_vehicles_waiting(vehicle_log) #Guarda la cantidad de vehiculos que devuelve la funcion que cuenta los vehiculos esperando.

for vehicle in vehicle_log:
    print(f"Vehicle {vehicle['vehicle_id']}: {vehicle['state']}")

#===========
#Imprime una tabla de control de las plazas, para saber el estado del parqueadero.
#===========
print()
print(f"Capacity: {MAX_CAPACITY} | Occupied: {occupied_spaces} | Availability: {availability_spaces} | Occupation:              {occupation_state}({occupation_rate:.1f}%) | Waiting: {vehicles_waiting}")
print()
total_simulation_time = time.time() - start
print(f"Simulation:{total_simulation_time:.4f}")
