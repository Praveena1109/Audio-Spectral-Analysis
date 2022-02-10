import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
plt.rcParams['figure.figsize']=[20,10]
plt.rcParams.update({'font.size':10})

BASE_FOLDER = "./Audio Data"
sound_file = "Sargam2.wav"
sa = "sa.wav"
re = "re.wav"
ga = "ga.wav"
ma = "ma.wav"
pa = "pa.wav"
da = "dha.wav"
ni = "ni.wav"
saa = "sa-2.wav"

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
    plt.subplot(2,4,i)
    plt.plot(f[1:f_bins], power_spectrum[1:f_bins])
    newX_mag1=remove_till_limit(X_mag,100,f_bins)
    print(f"Fundamental Frequency(Pitch) is {round(f[getFundamental(newX_mag1,f_bins)])} Hz") 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.title('Power Spectrum ' + f"Pitch = {round(f[getFundamental(newX_mag1,f_bins)])} Hz")

# plot_time_domain(voice)
plot_power_spectrum(voice_sa,1)
plot_power_spectrum(voice_re,2)
plot_power_spectrum(voice_ga,3)
plot_power_spectrum(voice_ma,4)
plot_power_spectrum(voice_pa,5)
plot_power_spectrum(voice_da,6)
plot_power_spectrum(voice_ni,7)
plot_power_spectrum(voice_saa,8)

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
plt.show()
