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

capacity = 100
occupied_spaces = 88

if occupied_spaces < capacity:
    occupied_spaces += 1
    print("entra") 
else:
    print("no entra")

available_spaces = capacity - occupied_spaces
occupied_rate = (occupied_spaces / capacity) * 100

if occupied_rate < 50:
    status = "Baja"
elif occupied_rate < 90:
    status = "Media"
else:
    status = "Alta"

print(f"Capacidad: {capacity} | Ocupados: {occupied_spaces} | Disponibles: {available_spaces} | Ocupacion: {status}({occupied_rate}%)")