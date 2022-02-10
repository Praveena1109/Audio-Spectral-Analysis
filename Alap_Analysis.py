import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
import wave
plt.rcParams['figure.figsize']=[20,10]
plt.rcParams.update({'font.size':9})

base="./Audio Data/"
voice, sr = librosa.load(base+"adish_alap_aroh_b1.wav")
voice1, _ = librosa.load(base+"alap1.wav")
voice2, _ = librosa.load(base+"alap2.wav")
voice3, _ = librosa.load(base+"alap3.wav")
voice4, _ = librosa.load(base+"alap4.wav")
voice5, _ = librosa.load(base+"alap5.wav")
voice6, _ = librosa.load(base+"alap6.wav")
voice7, _ = librosa.load(base+"alap7.wav")
voice8, _ = librosa.load(base+"alap8.wav")
voice9, _ = librosa.load(base+"alap9.wav")
voice10, _ = librosa.load(base+"alap10.wav")
voice11, _ = librosa.load(base+"alap11.wav")
voice12, _ = librosa.load(base+"alap12.wav")
def limitFreq(freq,size):
    for i,j in enumerate(freq):
        if j>size:
            return i
            break
def remove_till_limit(Xaxis,limit,maxBins):
    newX=[]
    for i in Xaxis[:maxBins]:
        if i<limit:
            newX.append(0)
        else:
            newX.append(i)
    return newX
def getFundamental(Xaxis,bins):
    for i,j in enumerate(Xaxis[1:bins]):
        if j>0:
            return i
def plot_time_domain(voice):
    plt.plot(voice)
    plt.xlabel('Time') 
    plt.ylabel('Amplitude')
    plt.title('Time Domain')
    plt.show()

def plot_power_spectrum(voice,i):
    X = np.fft.fft(voice)
    X_mag = np.absolute(X)
    power_spectrum = np.square(X_mag)
    f = np.linspace(0, sr, len(power_spectrum))
    f_bins=limitFreq(f,2000)
    plt.subplot(3,4,i)
    plt.plot(f[1:f_bins], power_spectrum[1:f_bins])
    newX_mag1=remove_till_limit(X_mag,500,f_bins)
    print(f"Fundamental Frequency(Pitch) is {round(f[getFundamental(newX_mag1,f_bins)])} Hz") 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.title('Power Spectrum ' + f"Pitch = {round(f[getFundamental(newX_mag1,f_bins)])} Hz")

# plot_time_domain(voice)
plot_power_spectrum(voice1,1)
plot_power_spectrum(voice2,2)
plot_power_spectrum(voice3,3)
plot_power_spectrum(voice4,4)
plot_power_spectrum(voice5,5)
plot_power_spectrum(voice6,6)
plot_power_spectrum(voice7,7)
plot_power_spectrum(voice8,8)
plot_power_spectrum(voice9,9)
plot_power_spectrum(voice10,10)
plot_power_spectrum(voice11,11)
plot_power_spectrum(voice12,12)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
plt.show()

