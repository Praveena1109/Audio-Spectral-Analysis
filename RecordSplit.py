import pyaudio
import wave
import time
import os

for _ in range(6):
    print("Select Tonic Note: ")
    tonic = int(input())
    print("Select Type: ")
    type = input()
    # audio = pyaudio.PyAudio()
    # stream = audio.open(format = pyaudio.paInt16, channels=1, rate = 44100, input=True, frames_per_buffer=1024)
    # print("Started recording")
    # print("Press S to stop recording")
    # frames = []
    # # timeout = 77  # [seconds]
    # # timeout_start = time.time()
    # # while time.time() < timeout_start + timeout:
    # #     data = stream.read(1024) 
    # #     frames.append(data)
    # try:
    #     while True:
    #         data = stream.read(1024)
    #         frames.append(data)
    # except KeyboardInterrupt:
    #     print("Done recording")
    # except Exception as e:
    #     print(str(e))
    # stream.stop_stream()
    # stream.close()
    # audio.terminate()
    # print("Finished Recording")

    folder_name = type+'_'+str(tonic)
    name=type+'_'+str(tonic)+'.wav' 

    # sound_file = wave.open(name,"wb")
    # sound_file.setnchannels(1)
    # sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    # sound_file.setframerate(44100)
    # sound_file.writeframes(b''.join(frames))
    # sound_file.close()
    # os.rename(name, f'AudioFiles/{name}')


    from pydub import AudioSegment
    from pydub.silence import split_on_silence
    import os
    path = f'AudioFiles/{name}'
    folder = f'AudioFiles/{folder_name}'

    # Define a function to normalize a chunk to a target amplitude.
    def match_target_amplitude(aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)
    try:
        # Create target Directory
        os.mkdir(folder)
        print("Directory " , folder ,  " Created ") 
    except FileExistsError:
        print("Directory " , folder ,  " already exists")

    # Load your audio.
    song = AudioSegment.from_wav(path)
    # Split track where the silence is 2 seconds or more and get chunks using 
    # the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        song, 
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = 100,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = -35
    )
    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=100)
        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk
        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -25.0)
        # Export the audio chunk with new bitrate.
        if len(str(i))==1:
            # print("Exporting sar0{0}.wav to {1}".format(i,name))
            normalized_chunk.export(
            "./{1}/sargam0{0}.wav".format(i,folder),
            bitrate = "192k",
            format = "wav"
        )
        else:
            # print("Exporting sar{0}.wav to {1}".format(i,name))
            normalized_chunk.export("./{1}/sargam{0}.wav".format(i,folder),
            bitrate = "192k",
            format = "wav"
        ) 

    for filename in sorted(os.listdir(folder)):
        f = os.path.join(folder, filename)   
        if os.path.getsize(f) < 25*1024:
            os.remove(f) 
        # print(f,' --> ',os.path.getsize(f))

    # count=1
    # for filename in sorted(os.listdir(folder)):
    #     old = os.path.join(folder, filename)
    #     new=f[:23]+f'Sargam{count}.wav'  
    #     try:
    #         os.rename(old,new)
    #         # print(old,new)
    #         count+=1
    #     except FileExistsError:
    #         print("File " , filename ,  " already exists")

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
    import warnings
    import json

    warnings.filterwarnings('ignore') 
    warnings.warn('Do not show this message')

    base="./AudioFiles/" + folder_name

    sar = []
    for filename in os.scandir(base):
        sar.append(filename.path)

    voice = []
    for j in range(len(sar)):
        voice1, sr = librosa.load(sar[j])
        voice.append(voice1)

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
            if j > 0.89:
                lis.append(i)
        val=[frequency[i] for i in lis]
        return sum(val)/len(val)

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
        return [midBand,highBand]

    def plot_power_spectrum(path,voice,i):
        X = np.fft.fft(voice)
        X_mag = np.absolute(X)
        power_spectrum = np.square(X_mag)
        f = np.linspace(0, sr, len(power_spectrum))
        f_bins=limitFreq(f,2000)
        pitch=round(pitchEstimator(path))
        Pitch.append(pitch)
        # print(f"Fundamental Frequency(Pitch) is {pitch} Hz") 
        plt.subplot(3,6,i)
        plt.plot(f[1:f_bins], power_spectrum[1:f_bins])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power')
        plt.title('Power Spectrum ' + f"Pitch = {pitch} Hz")

    plt.figure(1)
    plt.figure
    for j in range(len(sar)):
        plot_power_spectrum(sar[j],voice[j],j+1)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
    plt.show() 

    coordinates = []
    for j in range(len(sar)):
        coordinates.append(findCoordinates(sar[j],voice[j],j+1))

    grey_count = 0
    central_count = 0
    for coordinate in coordinates:
        if ( coordinate[1]>=0.9 and coordinate[0]<=0.1 ) or (coordinate[1] <=0.1 and coordinate[0] <=0.1) or (coordinate[1]<=0.2 and coordinate[0]>=0.8):
            grey_count+=1
        if (0.1<=coordinate[1]<= 0.5) and (0.2<=coordinate[0]<=0.7):
            central_count+=1
    
    filename = 'output1.json'

    if type =="Aroh":

        dictionary ={

            "tonic" : Pitch[0],
            "highest": [max(Pitch)],
            # "highest1" : [Pitch[10],coordinates[10][0],coordinates[10][1]],
            # "highest2": [Pitch[9],coordinates[9][0],coordinates[9][1]],
            "grey_count" : grey_count,
            "central_count" : central_count
        }

    else:
        dictionary ={

            "tonic" : Pitch[-1],
            "highest": [min(Pitch)],
            # "highest1" : [Pitch[10],coordinates[10][0],coordinates[10][1]],
            # "highest2": [Pitch[9],coordinates[9][0],coordinates[9][1]],
            "grey_count" : grey_count,
            "central_count" : central_count
        }

    with open(filename, "r") as file:
        data = json.loads(file.read())
    try:
        del data[base]
    except:
        pass
    data[base] = dictionary
    with open(filename, "w") as file:
        json.dump(data, file)

    data = np.array(coordinates)
    y, x = data.T
    # n=['sa','re','ga','ma','pa','dha','ni','sa`','re`','ga`','ma`','ga','re','sa']

    plt.figure(figsize=(25, 15))  
    plt.rcParams['font.size'] = '10' 

    triA1 = [ 0, 0.1, 0, 0 ] 
    triA2 = [ 0, 0, 0.1, 0 ] 
    triB1 = [ 0, 0.1, 0, 0 ]    
    triB2 = [ 0.9, 0.9, 1, 0.9]
    triC1 = [ 0.8,  0.8, 1.0, 0.8 ]
    triC2 = [ 0, 0.2, 0, 0 ]
    plt.fill(triA1, triA2, color='#BABABA')
    plt.fill(triB1, triB2, color='#BABABA')
    plt.fill(triC1, triC2, color='#BABABA')

    plt.scatter(x, y,s=50)
    plt.xlabel('Power in High Band',fontsize=18)
    plt.ylabel('Power in Mid Band',fontsize=18)
    plt.plot([1,0],[0,1], 'k-',linewidth=1)
    plt.plot([0,0.1],[0.9,0.9], 'k-',linewidth=1)
    plt.plot([0.1,0],[0,0.1], 'k-',linewidth=1)
    plt.plot([0.8,0.8],[0,0.2], 'k-',linewidth=1)

    plt.xlim(0,1)
    plt.ylim(0,1)

    # for i,j,k in zip(x,y,n):
    #     label = k
    #     plt.annotate(label,(i,j), textcoords="offset points", xytext=(0,10),ha='center') 

    plt.show()
    plt.close()


# import os
# import glob

# files = glob.glob('/YOUR/PATH/*')
# for f in files:
#     os.remove(f)