import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
BASE_FOLDER = "/Users/Praveena Acharya/Desktop/Audio Spectral Analysis"
sound_file = "somu.wav"

ipd.Audio(os.path.join(BASE_FOLDER, sound_file))

# load sounds
voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))
print(sr)
# Plot Time Domain signal
# Ploting FFT
X = np.fft.fft(voice)
def plot_magnitude_spectrum(signal, sr, f_ratio=1):
    plt.figure(figsize=(18, 15))
    plt.subplot(311)
    plt.plot(voice)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Time Domain')
    X = np.fft.fft(signal)
    X_mag = np.absolute(X)
    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag)*f_ratio)
    plt.subplot(313)
    plt.plot(f[:f_bins], X_mag[:f_bins])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Frequency Domain - Fourier Transform ')
    plt.show()
plot_magnitude_spectrum(voice, sr, 0.1)
