import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve
from scipy.fftpack import fft

# Inicialización de PyAudio
p = pyaudio.PyAudio()

# Definición de constantes
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
LIVE_PLOT_UPDATE = 0.1  # Intervalo de actualización del gráfico en segundos

# Función para calcular la autocorrelación
def autocorrelation(x):
    return fftconvolve(x, x[::-1], mode='full')

# Función para calcular la autocovarianza
def autocovariance(x):
    autocorr = autocorrelation(x)
    return autocorr / len(x) - np.mean(x) ** 2
    #n = len(x)
    #x_mean = np.mean(x)
    #autocov = np.array([np.sum((x[:n-k] - x_mean) * (x[k:] - x_mean)) / n for k in range(n)])
    #return autocov

# Función para calcular el espectro
def spectrum(x):
    return np.abs(fft(x)) # c

# Función para determinar si una señal es ruido blanco
def is_white_noise(spectrum, threshold):
    #print(spectrum)
    # Debes definir cómo determinar el umbral
    # return np.std(spectrum) < threshold
    return np.std(spectrum) < threshold

# Crear un gráfico en tiempo real
plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

# Función principal para procesar y mostrar la señal de audio
def process_and_plot(stream,ax):
    if not plt.fignum_exists(fig.number):
        # Si la ventana de la figura se ha cerrado, levanta una excepción para salir del bucle
        raise Exception("Plot window closed")
    
    raw_data = stream.read(CHUNK)
    data = np.frombuffer(raw_data, dtype=np.float32) # f 

    # Calculando autocorrelación y autocovarianza
    autocorr = autocorrelation(data) # y
    autocovar = autocovariance(data) # z

    # Calculando la FFT y el espectro
    spctrm = spectrum(autocovar)

    threshold = 1e-4
    white_noise = is_white_noise(spctrm,threshold)

    # Actualizando gráficos
    ax1.clear()
    ax1.plot(autocorr)
    ax1.set_title('Autocorrelación')

    ax2.clear()
    ax2.plot(autocovar, color='darkred')
    ax2.set_title('Autocovarianza')

    ax3.clear()
    ax3.plot(spctrm, color='red')
    ax3.set_title('Espectro')

    plt.subplots_adjust(hspace=1)

        # Determina el mensaje a mostrar en base a si se detectó ruido blanco o no
    message = "Detectado ruido blanco" if white_noise else "Detectada señal de información"
    # Añade el mensaje a la gráfica
    ax.text(0.5, 0.5, message, ha='center', va='center', transform=ax.transAxes, color='maroon', weight='bold')

    plt.subplots_adjust(hspace=1)
    plt.pause(LIVE_PLOT_UPDATE)
    return white_noise

# Abriendo el flujo de audio
stream = p.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

# Bucle principal para procesamiento continuo
try:
    while plt.fignum_exists(fig.number):  # Continúa mientras la ventana de la figura esté abierta
        is_noise = process_and_plot(stream, ax3)
        # Mostrar mensaje en consola
        message = "Detectado ruido blanco" if is_noise else "Detectada señal de información"
        print(message)
except Exception as e:
    # Manejar cualquier otra excepción que no sea KeyboardInterrupt
    print(str(e))
finally:
    # Detener y cerrar el flujo y PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.ioff()
    if plt.fignum_exists(fig.number):
        plt.close(fig)
