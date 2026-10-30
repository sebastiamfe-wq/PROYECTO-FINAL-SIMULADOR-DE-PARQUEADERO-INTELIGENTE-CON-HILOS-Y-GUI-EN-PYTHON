import tkinter as tk

from gui import ParkingApp


def main():
    """Abre la ventana del simulador."""
    root = tk.Tk()
    ParkingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()