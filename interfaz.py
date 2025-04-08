# main.py
import tkinter as tk
import distribuciones
from graficos import VentanaDist


def main():
    # Crear ventana principal
    root = tk.Tk()

    # Inicializar la aplicación
    app = VentanaDist(root, distribuciones)

    # Iniciar el bucle principal
    root.mainloop()


if __name__ == "__main__":
    main()