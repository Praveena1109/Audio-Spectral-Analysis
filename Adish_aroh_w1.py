import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
import wave
import crepe
from pyrsistent import v
from sklearn import preprocessing
plt.rcParams['figure.figsize']=[20,10]
plt.rcParams.update({'font.size':5})
from scipy.io import wavfile

base="./Adish_avroh_w1/"
sar0=base+"sargam0.wav"
sar1=base+"sargam1.wav"
sar2=base+"sargam3.wav"
sar3=base+"sargam4.wav"
sar4=base+"sargam5.wav"
sar5=base+"sargam6.wav"
sar6=base+"sargam7.wav"
sar7=base+"sargam9.wav"
sar8=base+"sargam10.wav"
sar9=base+"sargam11.wav"
sar10=base+"sargam12.wav"
sar11=base+"sargam13.wav"
sar12=base+"sargam14.wav"
sar13=base+"sargam16.wav"

voice, sr = librosa.load(sar0)
voice1, _ = librosa.load(sar0)
voice2, _ = librosa.load(sar1)
voice3, _ = librosa.load(sar2)
voice4, _ = librosa.load(sar3)
voice5, _ = librosa.load(sar4)
voice6, _ = librosa.load(sar5)
voice7, _ = librosa.load(sar6)
voice8, _ = librosa.load(sar7)
voice9, _ = librosa.load(sar8)
voice10, _ = librosa.load(sar9)
voice11, _ = librosa.load(sar10)
voice12, _ = librosa.load(sar11)
voice13, _ = librosa.load(sar12)
voice14, _ = librosa.load(sar13)

def limitFreq(freq,size):
    for i,j in enumerate(freq):
        if j>size:
            return i

def remove_till_limit(Xaxis,limit,maxBins):
    newX=[]
    for i in Xaxis[:maxBins]:
        if i<limit:
            newX.append(0)
        else:
            newX.append(i)
    return newX

def getFundamental(Xaxis,bins):
    for i,j in enumerate(Xaxis[20:bins]):
        if j>0:
            return i

# def getAllPower(Xaxis,bins):
#     harmonics = []
#     for i,j in enumerate(Xaxis[1:bins]):
#         if j>1:
#             harmonics.append(round(Xaxis[i]))
#     return harmonics

def getIndxTill(end,freq,indx,gap):
    for i in range(indx,len(freq)):
        max=end*gap+10
        if freq[i]>max:
            indx=i
            return indx
        
def getMaxPow(start,end,Yaxis):
    if sum(Yaxis[start:end])!=0:
        return max(Yaxis[start:end])
    else:
        return 0

def pitchEstimator(path):
    sr, audio = wavfile.read(path)
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True,step_size=100)
    lis=[]
    for i,j in enumerate(confidence): 
        if j > 0.92:
            lis.append(i)
    val=[frequency[i] for i in lis]
    return sum(val)/len(val)

# def getAllFrequency(Xaxis,f,bins):
#     harmonics = []
#     for i,j in enumerate(Xaxis[1:bins]):
#         if j>0:
#             harmonics.append(round(f[i]))
#     return harmonics
Pitch=[]
def findCoordinates(path,voice,i):
    X = np.fft.fft(voice)
    X_mag = np.absolute(X)
    power_spectrum = np.square(X_mag)
    f = np.linspace(0, sr, len(power_spectrum))
    f_bins=limitFreq(f,2000)
    newX_mag=remove_till_limit(power_spectrum,1000,f_bins) 
    pitch=Pitch[i-1]
    Harmonics=[]
    l=[1]
    totalSplit=int(round(2000/pitch))
    for i in range(totalSplit):
        index=getIndxTill(pitch,f,l[i],i+1) 
        l.append(index)
        Harmonics.append(getMaxPow(l[i],l[i+1],newX_mag))
    Harmonics = [i for i in Harmonics if i != 0]
    midBand = sum(Harmonics[1:4])/sum(Harmonics)
    highBand = sum(Harmonics[4:])/sum(Harmonics)
    print("Harmonics", Harmonics)
    print(midBand,highBand)
    return [midBand,highBand]
    # Harmonics = list(set(getAllFrequency(newX_mag1,f,f_bins)))
    # Harmonics.sort()
    # prev = Harmonics[0]
    # result = []
    # count = 0
    # s = 0
    # for i in range(len(Harmonics)):
    #     count+=1
    #     s = s + Harmonics[i]
    #     if prev + 100 < Harmonics[i]:
    #         result.append((s-Harmonics[i])//(count-1))
    #         count = 1
    #         s = Harmonics[i]
    #         prev = Harmonics[i]
    # result.append(s//count)
    # result.extend([0,0,0,0,0])
    # print(result)
    # midBand = sum(result[1:4])
    # highBand = sum(result[4:])

def plot_time_domain(voice):
    plt.plot(voice)
    plt.xlabel('Time') 
    plt.ylabel('Amplitude')
    plt.title('Time Domain')
    plt.show()

def plot_power_spectrum(path,voice,i):
    X = np.fft.fft(voice)
    X_mag = np.absolute(X)
    power_spectrum = np.square(X_mag)
    f = np.linspace(0, sr, len(power_spectrum))
    f_bins=limitFreq(f,2000)
    pitch=round(pitchEstimator(path))
    Pitch.append(pitch)
    # print(f"Fundamental Frequency(Pitch) is {pitch} Hz") 
    plt.subplot(2,7,i)
    plt.plot(f[1:f_bins], power_spectrum[1:f_bins])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.title('Power Spectrum ' + f"Pitch = {pitch} Hz")


# # plot_time_domain(voice)
plt.figure(1)
plt.figure
plot_power_spectrum(sar0,voice1,1)
plot_power_spectrum(sar1,voice2,2)
plot_power_spectrum(sar2,voice3,3)
plot_power_spectrum(sar3,voice4,4)
plot_power_spectrum(sar4,voice5,5)
plot_power_spectrum(sar5,voice6,6)
plot_power_spectrum(sar6,voice7,7)
plot_power_spectrum(sar7,voice8,8)
plot_power_spectrum(sar8,voice9,9)
plot_power_spectrum(sar9,voice10,10)
plot_power_spectrum(sar10,voice11,11)
plot_power_spectrum(sar11,voice12,12)
plot_power_spectrum(sar12,voice13,13)
plot_power_spectrum(sar13,voice14,14)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
plt.show()



coordinates = []
coordinates.append(findCoordinates(sar0,voice1,1))
coordinates.append(findCoordinates(sar1,voice2,2))
coordinates.append(findCoordinates(sar2,voice3,3))
coordinates.append(findCoordinates(sar3,voice4,4))
coordinates.append(findCoordinates(sar4,voice5,5))
coordinates.append(findCoordinates(sar5,voice6,6))
coordinates.append(findCoordinates(sar6,voice7,7))
coordinates.append(findCoordinates(sar7,voice8,8))
coordinates.append(findCoordinates(sar8,voice9,9))
coordinates.append(findCoordinates(sar9,voice10,10))
coordinates.append(findCoordinates(sar10,voice11,11))
coordinates.append(findCoordinates(sar11,voice12,12))
coordinates.append(findCoordinates(sar12,voice13,13))
coordinates.append(findCoordinates(sar13,voice14,14))
print("CO",coordinates)

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
plt.show()

# for cor in coordinates:
#     xmin = min(cor) 
#     xmax=max(cor)
#     for i, x in enumerate(cor):
#         cor[i] = (x-xmin) / (xmax-xmin)

# print(coordinates)

# X = np.array(coordinates)
# min_max_scaler = preprocessing.MinMaxScaler()
# scaled_x = min_max_scaler.fit_transform(X)
# print("NORM",scaled_x)


# print("NORM1",scaled_x)
data = np.array(coordinates)
y, x = data.T
# n=[f'sargam{i+1}' for i in range(14)]
n=['sa','re','ga','ma','pa','dha','ni','sa`','re`','ga`','ma`','ga','re','sa']


plt.figure(figsize=(25, 15))  
plt.rcParams['font.size'] = '15' 
plt.scatter(x, y,s=100)
plt.xlabel('Power in High Band',fontsize=18)
plt.ylabel('Power in Mid Band',fontsize=18)
plt.plot([1,0],[0,1], 'k-',linewidth=3)
plt.xlim(0,1)
plt.ylim(0,1)
for i,j,k in zip(x,y,n):
    label = k
    plt.annotate(label, # this is the text
                 (i,j), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center',) 


plt.show()
plt.close()

