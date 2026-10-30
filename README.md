# Simulador de parqueadero inteligente con Hilos y GUI en PYTHON

Simula un parqueadero con espacios limitados haciendo analogia a un Sistema Operativo,cada vehiculo representa un proceso que compite por un recurso finito.La concurrencia se modela con hilos (threads) y la sincronizacion con Lock y Semaphore

## Características

- La concurrencia se simula mediante hilos.
- La sincronizacion se realiza mediante Locks y Semaforos que evitan condiciones de carrera.
- La interfaz grafica muestra todo el proceso de acceder y liberar un espacio.

## Tecnologías

- Cada vehículo es un HILO independiente que llega, espera un espacio, se estaciona y sale.
- Si el parqueadero está lleno, el vehículo queda bloqueado hasta que otro salga, controlado por un semáforo.
- Un Lock garantiza la exclusión mutua sobre los datos compartidos y evita condiciones de carrera.
- Interfaz gráfica que muestra en tiempo real los espacios disponibles y ocupados y el estado de cada vehículo.
- Botones de control: Iniciar simulación, Agregar vehículo, Detener y Reiniciar.
- Métricas al final de la simulación: tiempo promedio de espera y utilización del parqueadero.
- El registro de cada simulacion queda registrado en un archivo .csv
- Los resultados pueden ser reproducibles mediante una semilla fija.

## Instalación y uso

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/sebastiamfe-wq/PROYECTO-FINAL-SIMULADOR-DE-PARQUEADERO-INTELIGENTE-CON-HILOS-Y-GUI-EN-PYTHON.git
   ```

2. Entrar a la carpeta:

   ```bash
   cd PROYECTO-FINAL-SIMULADOR-DE-PARQUEADERO-INTELIGENTE-CON-HILOS-Y-GUI-EN-PYTHON
   ```

3. Ejecutar:

   ```bash
   python src/main.py
   ```

## Configuración


## Autor

Juan Sebastian Jimenez Machado — Arquitectura se computadores y sistemas opertivos, Unoversidad EAN.