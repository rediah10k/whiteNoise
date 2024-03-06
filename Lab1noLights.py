import numpy as np
import scipy.signal as signal
import scipy.fftpack as fftpack
import pyaudio
import matplotlib.pyplot as plt

# Parámetros de la grabación
CHUNK_SIZE = 1024  # Tamaño del chunk de audio para procesar
FORMAT = pyaudio.paInt16  # Formato de audio
RATE = 44100  # Tasa de muestreo (puede ajustarse según sea necesario)
THRESHOLD = 10000  # Umbral para la detección de ruido blanco (ajusta según sea necesario)

# Inicializa PyAudio
audio = pyaudio.PyAudio()

# Abre el dispositivo de entrada de audio (micrófono)
stream = audio.open(format=FORMAT, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK_SIZE)

print("Analizando audio en tiempo real...")

try:
    while True:
        
        
        # Lee un chunk de audio desde el micrófono
        audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)

        # Calcula la autocovarianza de la señal de audio
        autocovariance = np.correlate(audio_data, audio_data, mode='full')

        # Aplica la Transformada Rápida de Fourier (FFT)
        fft_result = fftpack.fft(autocovariance)

        # Calcula la norma en cada punto de la FFT
        fft_norm = np.abs(fft_result)

        # Comprueba si la señal es ruido blanco
        is_white_noise = np.all(fft_norm < THRESHOLD)

        if is_white_noise:
            print("Ruido blanco detectado")
        else:
            print("Señal de audio detectada")
            
except KeyboardInterrupt:
    pass

print("Deteniendo la captura de audio...")

# Cierra el flujo de audio y termina PyAudio
stream.stop_stream()
stream.close()
audio.terminate()
