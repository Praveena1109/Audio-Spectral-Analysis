import kivy
import pyaudio
import wave
import time
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np
import crepe
from pyrsistent import v
from sklearn import preprocessing
from scipy.io import wavfile
import warnings
import json
from kivy.app import App
from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

#Define our different screens
class FirstWindow(Screen):
    tonic = ObjectProperty()
    type = ObjectProperty()

    def startrecord(self):
        tonic = self.tonic.text
        type = self.type.text
        audio = pyaudio.PyAudio()
        stream = audio.open(format = pyaudio.paInt16, channels=1, rate = 44100, input=True, frames_per_buffer=1024)
        print("Started recording")
        # print("Press CTRL+C to stop recording")
        frames = []
        try:
            while True:
                data = stream.read(1024)
                frames.append(data)
        except KeyboardInterrupt:
            print("Done recording")
        except Exception as e:
            print(str(e))
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Finished Recording")
        folder_name = type+'_'+str(tonic)
        name=type+'_'+str(tonic)+'.wav'
        print(name)
        sound_file = wave.open(name,"wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        print("Done")
        os.rename(name, f'AudioRecord/{name}')
        self.tonic.text = ""
        self.type.text =""


    def stoprecord(self):
        pass


    def saverecord(self):
        tonic = self.tonic.text
        type = self.type.text
        folder_name = type+'_'+str(tonic)
        name=type+'_'+str(tonic)+'.wav'
        path = f'AudioFiles/{name}'
        folder = f'AudioFiles/{folder_name}'
        def match_target_amplitude(aChunk, target_dBFS):
            ''' Normalize given audio chunk '''
            change_in_dBFS = target_dBFS - aChunk.dBFS
            return aChunk.apply_gain(change_in_dBFS)
        try:
            os.mkdir(folder)
            print("Directory " , folder ,  " Created ")
        except FileExistsError:
            print("Directory " , folder ,  " already exists")

        song = AudioSegment.from_wav(path)
        chunks = split_on_silence (
            song,
            min_silence_len = 100,
            silence_thresh = -35
        )
        for i, chunk in enumerate(chunks):
            silence_chunk = AudioSegment.silent(duration=100)
            audio_chunk = silence_chunk + chunk + silence_chunk
            normalized_chunk = match_target_amplitude(audio_chunk, -25.0)
            if len(str(i))==1:
                normalized_chunk.export(
                "./{1}/sargam0{0}.wav".format(i,folder),
                bitrate = "192k",
                format = "wav"
            )
            else:
                normalized_chunk.export("./{1}/sargam{0}.wav".format(i,folder),
                bitrate = "192k",
                format = "wav"
            )
        for filename in sorted(os.listdir(folder)):
            f = os.path.join(folder, filename)
            if os.path.getsize(f) < 80*1024:
                os.remove(f)

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
            time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True,step_size=1000)
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
            pitch=round(pitchEstimator(path))
            Pitch.append(pitch)
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
                "lowest": [min(Pitch)],
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

class SecondWindow(Screen):
    pass


class ThirdWindow(Screen):
    def analyserange(self):

        keyboard_keys = {
            82.40689 : "E2",
            87.30706 : "F2",
            92.49861 : "F♯2",
            97.99886 : "G2",
            103.8262 : "G♯2",
            110.0000 : "A2",
            116.5409 : "A♯2",
            123.4708 : "B2",
            130.8128 : "C3",
            138.5913 : "C♯3",
            146.8324 : "D3",
            155.5635 : "D♯3",
            164.8138 : "E3",
            174.6141 : "F3",
            184.9972 : "F♯3",
            195.9977 : "G3",
            207.6523 : "G♯3",
            220.0000 : "A3",
            233.0819 : "A♯3",
            246.9417 : "B3",
            261.6256 : "C4",
            277.1826 : "C♯4",
        }

        f = open('output1.json')

        data = json.load(f)

        a = "./AudioFiles/Aroh_120"
        b = "./AudioFiles/Avaroh_120"
        c = "./AudioFiles/Aroh_130"
        d = "./AudioFiles/Avaroh_130"
        e = "./AudioFiles/Aroh_140"
        f = "./AudioFiles/Avaroh_140"

        first_grey = data[a]["grey_count"] + data[b]["grey_count"]
        second_grey = data[c]["grey_count"] + data[d]["grey_count"]
        third_grey = data[e]["grey_count"] + data[f]["grey_count"]
        first_center = data[a]["central_count"] + data[b]["central_count"]
        second_center = data[c]["central_count"] + data[d]["central_count"]
        third_center = data[e]["central_count"] + data[f]["central_count"]
        if first_grey < second_grey:
            if first_grey <  third_grey:
                highest_note = data[a]["highest"][0]
                lowest_note = data[b]["lowest"][0]
                tonic_range1 =  data[a]["tonic"]
                tonic_range2 =  data[b]["tonic"]
            elif first_grey > third_grey:
                highest_note = data[e]["highest"][0]
                lowest_note = data[f]["lowest"][0]
                tonic_range1 =  data[e]["tonic"]
                tonic_range2 =  data[f]["tonic"]
            else:
                if first_center > third_center:
                    highest_note = data[a]["highest"][0]
                    lowest_note = data[b]["lowest"][0]
                    tonic_range1 =  data[a]["tonic"]
                    tonic_range2 =  data[b]["tonic"]
                elif third_center >= first_center:
                    highest_note = data[e]["highest"][0]
                    lowest_note = data[f]["lowest"][0]
                    tonic_range1 =  data[e]["tonic"]
                    tonic_range2 =  data[f]["tonic"]
        elif first_grey == second_grey:
            if first_center > second_center:
                    highest_note = data[a]["highest"][0]
                    lowest_note = data[b]["lowest"][0]
                    tonic_range1 =  data[a]["tonic"]
                    tonic_range2 =  data[b]["tonic"]
            elif second_center >= first_center:
                highest_note = data[c]["highest"][0]
                lowest_note = data[d]["lowest"][0]
                tonic_range1 =  data[c]["tonic"]
                tonic_range2 =  data[d]["tonic"]
        elif second_grey < third_grey:
            highest_note = data[c]["highest"][0]
            lowest_note = data[d]["lowest"][0]
            tonic_range1 =  data[c]["tonic"]
            tonic_range2 =  data[d]["tonic"]
        elif second_grey == third_grey:
            if third_center > second_center:
                highest_note = data[e]["highest"][0]
                lowest_note = data[f]["lowest"][0]
                tonic_range1 =  data[e]["tonic"]
                tonic_range2 =  data[b]["tonic"]
            elif second_center >= third_center:
                highest_note = data[c]["highest"][0]
                lowest_note = data[d]["lowest"][0]
                tonic_range1 =  data[c]["tonic"]
                tonic_range2 =  data[d]["tonic"]

        print(self.ids.tonicrange.text)
        self.ids.tonicrange.text = f'{tonic_range1} Hz - {tonic_range2} Hz'
        self.ids.lowestnote.text = f'{lowest_note} Hz'
        self.ids.highestnote.text = f'{highest_note} Hz'

        keys = list(keyboard_keys.keys())
        closest_key = keys[min(range(len(keys)), key = lambda i: abs(keys[i]-tonic_range1))]

        self.ids.closestkey.text = f'{closest_key} Hz'

        self.ids.keyboardkey.text = f'{keyboard_keys[closest_key]} Hz'


        # print("****************************")
        # print("TONIC RANGE: ", tonic_range1,"Hz","-", tonic_range2,"Hz")
        # print()
        # print("LOWEST NOTE: ",lowest_note,"Hz" )
        # print()
        # print("HIGHEST NOTE: ",highest_note,"Hz")
        # print()
        #
        # print("CLOSEST KEY FREQUENCY: ",closest_key,"Hz" )
        # print()
        # print("KEYBOARD KEY: ",keyboard_keys[closest_key])
        # print("*****************************")




class FourthWindow(Screen):
    pass
class FifthWindow(Screen):
    pass
class SixthWindow(Screen):
    pass
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('voiceanalysis.kv')

class VoiceApp(App):
    def build(self):

        return kv

if __name__=='__main__':
    VoiceApp().run()
