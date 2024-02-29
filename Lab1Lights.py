import sounddevice as sd
import numpy as np
import tkinter as tk
from threading import Thread
import pyaudio

CHUNK_SIZE = 1024  # Tamaño del chunk de audio para procesar
FORMAT = pyaudio.paInt16  # Formato de audio
RATE = 44100  # Tasa de muestreo (puede ajustarse según sea necesario)
THRESHOLD = 11000  # Umbral para la detección de ruido blanco (ajusta según sea necesario)
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=1, rate=RATE, input=True,
                    frames_per_buffer=CHUNK_SIZE)

def identify_white_noise(audio_chunk, threshold=0.5):
    fft_result = np.fft.fft(audio_chunk)
    freqs = np.fft.fftfreq(len(fft_result))
    freqs = freqs[:len(freqs) // 2]
    freq_band_energy = np.sum(np.abs(fft_result[:len(fft_result) // 2]) ** 2)
    # Lee un chunk de audio desde el micrófono
    audio_data = np.frombuffer(stream.read(CHUNK_SIZE), dtype=np.int16)

        # Calcula la autocovarianza de la señal de audio
    autocovariance = np.correlate(audio_data, audio_data, mode='full')
    
    if freq_band_energy < threshold:
        return True
    else:
        return False

def audio_callback(indata, frames, time, status):
    if status:
        print("Error:", status)
    
    is_white_noise = identify_white_noise(indata)
    if is_white_noise:
        canvas.config(bg="red")
    else:
        canvas.config(bg="green")

def stop_capture():
    global capture_running
    capture_running = False

def capture_audio():
    global capture_running
    capture_running = True
    
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        print("Escuchando...")
        while capture_running:
            sd.sleep(int(duration * 1000))

# Configura los parámetros de audio
duration = 180
sample_rate = 44100

# Configura la interfaz gráfica
root = tk.Tk()
root.title("Detector de Ruido Blanco")

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

stop_button = tk.Button(root, text="Finalizar", command=stop_capture)
stop_button.pack()

# Inicia la captura de audio en un hilo separado
audio_thread = Thread(target=capture_audio)
audio_thread.start()

root.mainloop()
