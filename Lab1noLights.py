import numpy as np
import scipy.fftpack as fftpack
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parámetros de la grabación
CHUNK_SIZE = 1024  # Tamaño del chunk de audio para procesar
FORMAT = pyaudio.paInt16  # Formato de audio
RATE = 44100  # Tasa de muestreo
THRESHOLD = 10000  # Umbral para detección de ruido blanco

# Inicializa PyAudio
audio = pyaudio.PyAudio()

# Abre el dispositivo de entrada de audio (micrófono), parametro input_device_index=2 para micro pc o igual a 7 para externo de droidcam
stream = audio.open(format=FORMAT, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK_SIZE)

fig, ax = plt.subplots()
x = np.arange(-CHUNK_SIZE + 1, CHUNK_SIZE, 1)
line, = ax.plot(x, np.zeros_like(x))
ax.set_ylim(0, 60000)  # Ajusta este valor según sea necesario

def init():
    line.set_ydata(np.zeros_like(x))
    return line,

def is_white_noise(fft_norm, threshold=THRESHOLD):
    # Considera ruido blanco si todas las frecuencias tienen una norma por debajo del umbral
    return np.all(fft_norm < threshold)

def update(frame):
    audio_data = np.frombuffer(stream.read(CHUNK_SIZE, exception_on_overflow=False), dtype=np.int16)
    autocovariance = np.correlate(audio_data, audio_data, mode='full')
    

    # FFT y norma para detección de ruido blanco
    fft_result = fftpack.fft(autocovariance)
    fft_norm = np.abs(fft_result)
    line.set_ydata(fft_norm)
    if is_white_noise(fft_norm):
        print("Ruido blanco detectado")
    else:
        print("Señal de audio detectada")
    
    return line,

ani = FuncAnimation(fig, update, init_func=init, blit=True, repeat=False, frames=None)

plt.show()

# Detiene y cierra el flujo de audio
stream.stop_stream()
stream.close()
audio.terminate()