import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Creamos la figura y el objeto de ejesfg
fig, ax = plt.subplots()
# Creamos una línea vacía que actualizaremos más adelante
line, = ax.plot([], [], lw=2)

# Definimos la función para inicializar la gráfica
def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return line,

# Definimos la función para actualizar la gráfica
def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    line.set_data(xdata, ydata)
    return line,

# Inicializamos los datos
xdata, ydata = [], []

# Creamos una animación con la función de actualización
ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 10),
                    init_func=init, blit=True)

# Mostramos la gráfica
plt.show()
