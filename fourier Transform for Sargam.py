import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
BASE_FOLDER = "/Users/Praveena Acharya/Desktop/Audio Spectral Analysis/Audio Data"
sound_file = "Sargam2.wav"
sa = "sa.wav"
re = "re.wav"
ga = "ga.wav"
ma = "ma.wav"
pa = "pa.wav"
da = "dha.wav"
ni = "ni.wav"
saa = "sa-2.wav"

ipd.Audio(os.path.join(BASE_FOLDER, sound_file))
ipd.Audio(os.path.join(BASE_FOLDER, sa))
ipd.Audio(os.path.join(BASE_FOLDER, re))
ipd.Audio(os.path.join(BASE_FOLDER, ga))
ipd.Audio(os.path.join(BASE_FOLDER, ma))
ipd.Audio(os.path.join(BASE_FOLDER, pa))
ipd.Audio(os.path.join(BASE_FOLDER, da))
ipd.Audio(os.path.join(BASE_FOLDER, ni))
ipd.Audio(os.path.join(BASE_FOLDER, saa))
# load sounds
voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))
voice_sa, _ = librosa.load(os.path.join(BASE_FOLDER, sa))
voice_re, _ = librosa.load(os.path.join(BASE_FOLDER, re))
voice_ga, _ = librosa.load(os.path.join(BASE_FOLDER, ga))
voice_ma, _ = librosa.load(os.path.join(BASE_FOLDER, ma))
voice_pa, _ = librosa.load(os.path.join(BASE_FOLDER, pa))
voice_da, _ = librosa.load(os.path.join(BASE_FOLDER, da))
voice_ni, _ = librosa.load(os.path.join(BASE_FOLDER, ni))
voice_saa, _ = librosa.load(os.path.join(BASE_FOLDER, saa))

print(sr)
# Plot Time Domain signal
# Ploting FFT

def plot_magnitude_spectrum(signal, voice_sa,voice_re,voice_ga,voice_ma,voice_pa,voice_da,voice_ni,voice_saa, sr, f_ratio=1):

    plot1 = plt.subplot2grid((4,4),(0,0), colspan=4)
    plot2 = plt.subplot2grid((4,4),(1,0), colspan=4)
    plot3 = plt.subplot2grid((4,4),(2,0))
    plot4 = plt.subplot2grid((4,4),(2,1))
    plot5 = plt.subplot2grid((4,4),(2,2))
    plot6 = plt.subplot2grid((4,4),(2,3))
    plot7 = plt.subplot2grid((4,4),(3,0))
    plot8 = plt.subplot2grid((4,4),(3,1))
    plot9 = plt.subplot2grid((4,4),(3,2))
    plot10 = plt.subplot2grid((4,4),(3,3))

    plot1.plot(signal)
    plot1.set_xlabel('Time')
    plot1.set_ylabel('Amplitude')
    plot1.set_title('Time Domain')

    X = np.fft.fft(signal)
    print(len(signal))
    X_mag = np.absolute(X)
    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag)*f_ratio)
    print(f_bins)
    plot2.plot(f[:f_bins], X_mag[:f_bins])
    plot2.set_xlabel('Frequency (Hz)')
    plot2.set_ylabel('Amplitude')
    plot2.set_title('Frequency Domain - Fourier Transform ')

    X1 = np.fft.fft(voice_sa)
    X1_mag = np.absolute(X1)
    f1 = np.linspace(0, sr, len(X1_mag))
    f1_bins = int(len(X1_mag)*f_ratio)
    plot3.plot(f1[:f1_bins], X1_mag[:f1_bins])
    plot3.set_xlabel('Frequency (Hz)')
    plot3.set_ylabel('Amplitude')
    plot3.set_title('Sa ')

    X2 = np.fft.fft(voice_re)
    X2_mag = np.absolute(X2)
    f2 = np.linspace(0, sr, len(X2_mag))
    f2_bins = int(len(X2_mag)*f_ratio)
    plot4.plot(f2[:f2_bins], X2_mag[:f2_bins])
    plot4.set_xlabel('Frequency (Hz)')
    plot4.set_ylabel('Amplitude')
    plot4.set_title('Re ')

    X3 = np.fft.fft(voice_ga)
    X3_mag = np.absolute(X3)
    f3 = np.linspace(0, sr, len(X3_mag))
    f3_bins = int(len(X3_mag)*f_ratio)
    plot5.plot(f3[:f3_bins], X3_mag[:f3_bins])
    plot5.set_xlabel('Frequency (Hz)')
    plot5.set_ylabel('Amplitude')
    plot5.set_title('Ga')

    X4 = np.fft.fft(voice_ma)
    X4_mag = np.absolute(X4)
    f4 = np.linspace(0, sr, len(X4_mag))
    f4_bins = int(len(X4_mag)*f_ratio)
    plot6.plot(f4[:f4_bins], X4_mag[:f4_bins])
    plot6.set_xlabel('Frequency (Hz)')
    plot6.set_ylabel('Amplitude')
    plot6.set_title('Ma')

    X5 = np.fft.fft(voice_pa)
    X5_mag = np.absolute(X5)
    f5 = np.linspace(0, sr, len(X5_mag))
    f5_bins = int(len(X5_mag)*f_ratio)
    plot7.plot(f5[:f5_bins], X5_mag[:f5_bins])
    plot7.set_xlabel('Frequency (Hz)')
    plot7.set_ylabel('Amplitude')
    plot7.set_title('Pa ')

    X6 = np.fft.fft(voice_da)
    X6_mag = np.absolute(X6)
    f6 = np.linspace(0, sr, len(X6_mag))
    f6_bins = int(len(X6_mag)*f_ratio)
    plot8.plot(f6[:f6_bins], X6_mag[:f6_bins])
    plot8.set_xlabel('Frequency (Hz)')
    plot8.set_ylabel('Amplitude')
    plot8.set_title('Dha ')

    X7 = np.fft.fft(voice_ni)
    X7_mag = np.absolute(X7)
    f7 = np.linspace(0, sr, len(X7_mag))
    f7_bins = int(len(X7_mag)*f_ratio)
    plot9.plot(f7[:f7_bins], X7_mag[:f7_bins])
    plot9.set_xlabel('Frequency (Hz)')
    plot9.set_ylabel('Amplitude')
    plot9.set_title('Ni')

    X8 = np.fft.fft(voice_saa)
    X8_mag = np.absolute(X8)
    f8 = np.linspace(0, sr, len(X8_mag))
    f8_bins = int(len(X8_mag)*f_ratio)
    plot10.plot(f8[:f8_bins], X8_mag[:f8_bins])
    plot10.set_xlabel('Frequency (Hz)')
    plot10.set_ylabel('Amplitude')
    plot10.set_title('Sa')

    plt.tight_layout()
    plt.show()


plot_magnitude_spectrum(voice,voice_sa,voice_re,voice_ga,voice_ma,voice_pa,voice_da,voice_ni,voice_saa, sr, 0.05)
