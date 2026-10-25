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


capacity = 10 #Se le asigna la capacidad que va a tener el parquadero.
occupied_spaces = 0 #Representa los espacios que es van a ocupar, por eso se inicializa en cero. 
available_spaces = capacity - occupied_spaces #Calcula los espacios libres en el parqueadero.  
vehicles_waiting = 0 #Se le asigna el numero de vehiculos esperando a entrar. 
total_vehicles = 200 #Variable que simula el total de vehiculos que van a entrar al parqueadero.    

#===========
#El ciclo cumple la funcion de permitir que un vehiculo entre o no.
#===========
for vehiculo in range(1, total_vehicles + 1):
    if occupied_spaces < capacity:
        occupied_spaces += 1
        available_spaces -= 1
        print(f"Vehiculo {vehiculo} entra | Ocupados: {occupied_spaces} | Disponibles: {available_spaces}") 
    else:
        vehicles_waiting += 1
        print(f"Vehiculo {vehiculo} no entra, parqueadero lleno")

#===========
#La condicion evalua respecto al porcentaje de ocupacion (occupied_rate) si la ocupacion es baja, media o alta.
#===========
occupied_rate = (occupied_spaces / capacity) * 100
if occupied_rate < 50:
    status = "Baja"
elif occupied_rate < 90:
    status = "Media"
else:
    status = "Alta"

#===========
#Imprime una tabla de control de las plazas, para saber es estado del parqueadero.
#===========
print(f"Capacidad: {capacity} | Ocupados: {occupied_spaces} | Disponibles: {available_spaces} | Ocupacion: {status}({occupied_rate:.1f}%) | Esperando: {vehicles_waiting}")