# visualizador.py
import matplotlib.pyplot as plt


def crear_histograma(datos, titulo, xlabel="Valor", ylabel="Frecuencia", bins=50, color='skyblue'):
    """
    Función para crear un histograma con matplotlib

    Args:
        datos: Lista de datos para el histograma
        titulo: Título del gráfico
        xlabel: Etiqueta del eje X
        ylabel: Etiqueta del eje Y
        bins: Número de contenedores/intervalos
        color: Color de las barras

    Returns:
        Figure, Axes: Objetos de matplotlib para su uso en interfaces
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(datos, bins=bins, alpha=0.7, color=color, edgecolor='black')
    ax.set_title(f"{titulo}\nIntervalos: {bins}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y', alpha=0.75)
    fig.tight_layout()

    return fig, ax


def mostrar_histograma(datos, titulo, xlabel="Valor", ylabel="Frecuencia", bins=50, color='skyblue'):
    """
    Crea y muestra un histograma con matplotlib

    Args:
        datos: Lista de datos para el histograma
        titulo: Título del gráfico
        xlabel: Etiqueta del eje X
        ylabel: Etiqueta del eje Y
        bins: Número de contenedores/intervalos
        color: Color de las barras
    """
    fig, ax = crear_histograma(datos, titulo, xlabel, ylabel, bins, color)
    plt.show()