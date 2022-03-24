import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
from sklearn import preprocessing
plt.rcParams['figure.figsize']=[20,10]
plt.rcParams.update({'font.size':10})

BASE_FOLDER = "./Audio Data"
sound_file = "Sargam2VC.wav"
sa = "Sargam1.wav"
re = "Sargam2.wav"
ga = "Sargam3.wav"
ma = "Sargam4.wav"
pa = "Sargam5.wav"
da = "Sargam6.wav"
ni = "Sargam7.wav"
saa = "Sargam8.wav"

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

def findCoordinates(voice,i):
    X = np.fft.fft(voice)
    X_mag = np.absolute(X)
    power_spectrum = np.square(X_mag)
    f = np.linspace(0, sr, len(power_spectrum))
    f_bins=limitFreq(f,2000)
    # f_bins = len(f)//2
    # newX_mag1=remove_till_limit(power_spectrum,100,f_bins)
    newX_mag1=remove_till_limit(power_spectrum,1000,f_bins)
    pitch = round(f[getFundamental(newX_mag1,f_bins)])
    print(pitch)
    totalSplit=int(round(f_bins/pitch))
    Harmonics=[]
    l=[1]
    print(totalSplit)
    for i in range(totalSplit):
        index=getIndxTill(pitch,f,l[i],i+1) 
        l.append(index)
        Harmonics.append(getMaxPow(l[i],l[i+1],newX_mag1))
    Harmonics = [i for i in Harmonics if i != 0]
    # xmin = min(Harmonics) 
    # xmax=max(Harmonics)
    # for i, x in enumerate(Harmonics):
    #     Harmonics[i] = (x-xmin) / (xmax-xmin)
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

# def plot_time_domain(voice):
#     plt.plot(voice)
#     plt.xlabel('Time') 
#     plt.ylabel('Amplitude')
#     plt.title('Time Domain')
#     plt.show()

def plot_power_spectrum(voice,i):
    X = np.fft.fft(voice)
    X_mag = np.absolute(X)
    power_spectrum = np.square(X_mag)
    f = np.linspace(0, sr, len(power_spectrum))
    f_bins=limitFreq(f,2000)
    # f_bins = len(f)
    plt.subplot(2,4,i)
    plt.plot(f[1:f_bins], power_spectrum[1:f_bins])
    newX_mag1=remove_till_limit(power_spectrum,100,f_bins)
    print(f"Fundamental Frequency(Pitch) is {round(f[getFundamental(newX_mag1,f_bins)])} Hz") 
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power')
    plt.title('Power Spectrum ' + f"Pitch = {round(f[getFundamental(newX_mag1,f_bins)])} Hz")


# plot_power_spectrum(voice_sa,1)
# plot_power_spectrum(voice_re,2)
# plot_power_spectrum(voice_ga,3)
# plot_power_spectrum(voice_ma,4)
# plot_power_spectrum(voice_pa,5)
# plot_power_spectrum(voice_da,6)
# plot_power_spectrum(voice_ni,7)
# plot_power_spectrum(voice_saa,8)

coordinates = []
coordinates.append(findCoordinates(voice_sa,1))
coordinates.append(findCoordinates(voice_re,2))
coordinates.append(findCoordinates(voice_ga,3))
coordinates.append(findCoordinates(voice_ma,4))
coordinates.append(findCoordinates(voice_pa,5))
coordinates.append(findCoordinates(voice_da,6))
coordinates.append(findCoordinates(voice_ni,7))
coordinates.append(findCoordinates(voice_saa,8))

# print("CO",coordinates)

# X = np.array(coordinates)
# min_max_scaler = preprocessing.MinMaxScaler()
# scaled_x = min_max_scaler.fit_transform(X)
# print("NORM",scaled_x)

data = np.array(coordinates)
x, y = data.T
n=['sa','re','ga','ma','pa','dha','ni',"saa'"]
plt.figure(figsize=(25, 15))  
plt.rcParams['font.size'] = '15' 

plt.scatter(y, x,s=100)
plt.xlabel('Power in High Band',fontsize=18)
plt.ylabel('Power in Mid Band',fontsize=18)
plt.plot([1,0],[0,1], 'k-',linewidth=3)
plt.xlim(0,1)
plt.ylim(0,1)
for i,j,k in zip(x,y,n):
    label = k
    plt.annotate(label, # this is the text
                 (j,i), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,10), # distance from text to points (x,y)
                 ha='center',) 
    

plt.show()

# plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
# plt.show()



# Harmonics = [1780894.851049973, 659547.3812550107, 101860.94816857947, 395785.09614056116, 1074063.9075481428, 110498.13689748544, 66386.60601599705, 136424.5188047195, 131285.65511382007]
# first = Harmonics[0]/sum(Harmonics)
# print(first)
# mid= sum(Harmonics[1:4])/sum(Harmonics)
# high = sum(Harmonics[4:])/sum(Harmonics)

# print(first+mid+high)