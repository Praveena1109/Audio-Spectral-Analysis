import numpy as np                 # for handling large arrays
import pandas as pd                # for data manipulation and analysis
import os                          # for accessing local files
import IPython.display as ipd
import librosa.display             # librosa plot functions
import matplotlib.pyplot as plt    # plotting with Matlab functionality
import librosa
from tkinter.tix import Select
import pyaudio
import wave
import time

print("Enter your name: ")
name = input()
audio = pyaudio.PyAudio()
stream = audio.open(format = pyaudio.paInt16, channels=1, rate = 44100, input=True, frames_per_buffer=1024)
print("Recording started for 15 secs")
frames = []
timeout = 15  # [seconds]
timeout_start = time.time()
while time.time() < timeout_start + timeout:
    data = stream.read(1024)
    frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()

print("Finished Recording")

sound_file = wave.open(name+".wav","wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b''.join(frames))
sound_file.close()


BASE_FOLDER = "../Audio Data"
sound_file = "adish_alap_aroh_b1.wav"

ipd.Audio(os.path.join(BASE_FOLDER, sound_file))

# load sounds
voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))


frame_length = 1024
hop_length = 512
features = []

# Zcr
zcr = librosa.feature.zero_crossing_rate(voice, frame_length=frame_length, hop_length=hop_length, center=True)[0]
mean_zcr = np.mean(zcr)
print(mean_zcr)
features.append(mean_zcr)

# Energy
e = np.sum(voice**2)
features.append(e)

# RMSE
rmse = librosa.feature.rms(voice, frame_length=frame_length, hop_length=hop_length, center=True)[0]
mean_rmse = np.mean(rmse)
print(mean_rmse)
features.append(mean_rmse)

# Beats Per Minute
tempo = librosa.beat.tempo(voice)[0]
features.append(tempo)