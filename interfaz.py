# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from chi_cuadrado import chi_cuadrado_test


class VentanaDist:
    def __init__(self, root, distribuciones):
        # Guardar referencia a las funciones de distribución
        self.distribuciones = distribuciones

        # Configuración de la ventana principal
        self.root = root
        self.root.title("Visualizador de Distribuciones")
        self.root.geometry("900x700")

        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para controles
        control_frame = ttk.LabelFrame(main_frame, text="Parámetros", padding="10")
        control_frame.pack(fill=tk.X, pady=10)

        # Selección de distribución
        ttk.Label(control_frame, text="Tipo de Distribución:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dist_type = ttk.Combobox(control_frame, values=["Normal", "Uniforme", "Poisson", "Exponencial"],
                                      state="readonly")
        self.dist_type.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.dist_type.current(0)
        self.dist_type.bind("<<ComboboxSelected>>", self.update_parameter_fields)

        # Frame para parámetros dinámicos
        self.param_frame = ttk.Frame(control_frame, padding="5")
        self.param_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Parámetro de número de muestras
        ttk.Label(control_frame, text="Número de muestras:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.n_samples = ttk.Entry(control_frame)
        self.n_samples.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.n_samples.insert(0, "1000")

        # Parámetro de número de intervalos (bins)
        ttk.Label(control_frame, text="Número de intervalos:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.n_bins = ttk.Entry(control_frame)
        self.n_bins.grid(row=3, column=1, sticky=tk.W, pady=5)
        self.n_bins.insert(0, "50")


        #etiqueta para la aceptacion
        ttk.Label(control_frame, text="Aceptacion (α):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.alpha_entry = ttk.Entry(control_frame)
        self.alpha_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.alpha_entry.insert(0, "0.05")

        # Botón generar
        ttk.Button(control_frame, text="Generar Distribución", command=self.generate_distribution).grid(row=5, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)



        # Frame para el gráfico
        self.plot_frame = ttk.LabelFrame(main_frame, text="Histograma", padding="10")
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Crear figura de matplotlib
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        # Incorporar la figura a Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Inicializar parámetros
        self.param_entries = {}
        self.update_parameter_fields()

    def update_parameter_fields(self, event=None):
        # Limpiar frame de parámetros
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        self.param_entries = {}
        dist = self.dist_type.get()

        if dist == "Normal":
            ttk.Label(self.param_frame, text="Media:").grid(row=0, column=0, sticky=tk.W, pady=5)
            media_entry = ttk.Entry(self.param_frame)
            media_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
            media_entry.insert(0, "0")
            self.param_entries["media"] = media_entry

            ttk.Label(self.param_frame, text="Desviación:").grid(row=1, column=0, sticky=tk.W, pady=5)
            desv_entry = ttk.Entry(self.param_frame)
            desv_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
            desv_entry.insert(0, "1")
            self.param_entries["desviacion"] = desv_entry

        elif dist == "Uniforme":
            ttk.Label(self.param_frame, text="Mínimo (a):").grid(row=0, column=0, sticky=tk.W, pady=5)
            a_entry = ttk.Entry(self.param_frame)
            a_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
            a_entry.insert(0, "0")
            self.param_entries["a"] = a_entry

            ttk.Label(self.param_frame, text="Máximo (b):").grid(row=1, column=0, sticky=tk.W, pady=5)
            b_entry = ttk.Entry(self.param_frame)
            b_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
            b_entry.insert(0, "1")
            self.param_entries["b"] = b_entry

        elif dist == "Poisson":
            ttk.Label(self.param_frame, text="Media (λ):").grid(row=0, column=0, sticky=tk.W, pady=5)
            lambda_entry = ttk.Entry(self.param_frame)
            lambda_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
            lambda_entry.insert(0, "5")
            self.param_entries["media"] = lambda_entry

        elif dist == "Exponencial":
            ttk.Label(self.param_frame, text="Lambda (λ = 1/media):").grid(row=0, column=0, sticky=tk.W, pady=5)
            lambda_entry = ttk.Entry(self.param_frame)
            lambda_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
            lambda_entry.insert(0, "1")
            self.param_entries["lambda"] = lambda_entry

    def generate_distribution(self):
        try:
            # Obtener número de muestras y de intervalos
            n = int(self.n_samples.get())
            bins = int(self.n_bins.get())

            if n <= 0:
                raise ValueError("El número de muestras debe ser positivo")
            if bins <= 0:
                raise ValueError("El número de intervalos debe ser positivo")

            # Obtener tipo de distribución
            dist_type = self.dist_type.get()

            # Generar datos según la distribución seleccionada
            datos = []
            if dist_type == "Normal":
                media = float(self.param_entries["media"].get())
                desviacion = float(self.param_entries["desviacion"].get())
                if desviacion <= 0:
                    raise ValueError("La desviación debe ser positiva")
                datos = self.distribuciones.normal(n, media, desviacion)
                titulo = f"Distribución Normal (μ={media}, σ={desviacion})"

            elif dist_type == "Uniforme":
                a = float(self.param_entries["a"].get())
                b = float(self.param_entries["b"].get())
                if a >= b:
                    raise ValueError("El valor mínimo debe ser menor que el máximo")
                datos = self.distribuciones.uniforme(n, a, b)
                titulo = f"Distribución Uniforme (a={a}, b={b})"

            elif dist_type == "Poisson":
                media = float(self.param_entries["media"].get())
                if media <= 0:
                    raise ValueError("La media debe ser positiva")
                datos = self.distribuciones.poisson(n, media)
                titulo = f"Distribución Poisson (λ={media})"

            elif dist_type == "Exponencial":
                lmbda = float(self.param_entries["lambda"].get())
                if lmbda <= 0:
                    raise ValueError("Lambda debe ser positivo")
                datos = self.distribuciones.exponencial(n, lmbda)
                titulo = f"Distribución Exponencial (λ={lmbda})"

            for dato in datos:
                print(dato)

            # Generar histograma
            self.ax.clear()
            self.ax.hist(datos, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
            self.ax.set_title(titulo)
            self.ax.set_xlabel("Valor")
            self.ax.set_ylabel("Frecuencia")
            self.ax.grid(axis='y', alpha=0.75)



            # Añadir información del número de intervalos al título
            self.ax.set_title(f"{titulo}\nIntervalos: {bins}")

            # Actualizar el canvas
            self.figure.tight_layout()
            self.canvas.draw()

            # Nivel de significancia
            alpha = float(self.alpha_entry.get())
            params = (0,0)
            # Realizar prueba chi-cuadrado
            if dist_type == "Normal":
                params = (media, desviacion)
            elif dist_type == "Uniforme":
                params = (a, b)
            elif dist_type == "Poisson":
                params = (media,)
            elif dist_type == "Exponencial":
                params = (lmbda,)

            chi2_calculado, chi2_tabla, gl = chi_cuadrado_test(datos, bins, alpha, dist_type, params)

            if not chi2_calculado:
                raise ValueError("no hay suficientes grados de libertad para calcular chi2")
            if chi2_calculado <= chi2_tabla:
                resultado = "Distribución **aceptada**"
            else:
                resultado = "Distribución **rechazada**"

            messagebox.showinfo(
                "Resultado del Test Chi-cuadrado",
                f"{resultado}\n\n"
                f"χ² calculado: {chi2_calculado:.3f}\n"
                f"χ² crítico (α={alpha}, gl={gl}): {chi2_tabla:.3f}\n"
            )

        except ValueError as e:
            messagebox.showerror("Error", str(e))
