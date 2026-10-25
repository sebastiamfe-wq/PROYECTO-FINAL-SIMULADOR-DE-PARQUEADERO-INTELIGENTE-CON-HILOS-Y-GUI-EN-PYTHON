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

def calc_availability(capacity, occupied): #Calcula los espacios libres en el parqueadero.
    return capacity - occupied 

def calc_occupation_rate(capacity, occupied): #Calcula el porcentaje de ocupacion del parqueader.
    percentage = (occupied / capacity) * 100
    return percentage

def calc_occupation_status(percentage): #Retorna el estado de ocupacion con base en el porcentaje de ocupacion.
    if percentage < 50:
        status = "Baja"
    elif percentage < 90:
        status = "Media"
    else:
        status = "Alta"
    return status


CAPACITY = 10 #Se le asigna la capacidad que va a tener el parquadero.
TOTAL_VEHICLES = 15 #Variable que simula el total de vehiculos que van a entrar al parqueadero. 
occupied_spaces = 0 #Representa los espacios que es van a ocupar, por eso se inicializa en cero. 
vehicles_waiting = 0 #Se le asigna el numero de vehiculos esperando a entrar, pero se inicializa en cero. 

#===========
#El ciclo cumple la funcion de permitir que un vehiculo entre o no.
#===========
for vehiculo in range(1, TOTAL_VEHICLES + 1):
    if occupied_spaces < CAPACITY:
        occupied_spaces += 1
        print(f"Vehiculo {vehiculo} entra | Ocupados: {occupied_spaces} | Disponibles: {calc_availability(CAPACITY, occupied_spaces)}") 
    else:
        vehicles_waiting += 1
        print(f"Vehiculo {vehiculo} no entra, parqueadero lleno")

#===========
#Estas variables guardan lo que retornan las dos funciones de ocupacion.
#===========
disponibility = calc_availability(CAPACITY, occupied_spaces)
rate = calc_occupation_rate(CAPACITY, occupied_spaces)
status = calc_occupation_status(rate)

#===========
#Imprime una tabla de control de las plazas, para saber es estado del parqueadero.
#===========
print(f"Capacidad: {CAPACITY} | Ocupados: {occupied_spaces} | Disponibles: {disponibility} | Ocupacion: {status}({rate:.1f}%) | Esperando: {vehicles_waiting}")