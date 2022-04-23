# IMPORTS

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
import pandas as pd
import seaborn as sns
import sklearn
import crepe
import signal
from pyrsistent import v
from sklearn import preprocessing
from scipy.io import wavfile
import warnings
import recorder
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

# DEFINED WINDOWS

# FIRST WINDOW - RECORDING AND SAVING

class FirstWindow(Screen):
    tonic = ""
    type = ""
    def checkbox_click(self, instance, value, selected):
        if value == True:
             FirstWindow.tonic = selected
        else:
            FirstWindow.tonic = ""

        print(FirstWindow.tonic)

    def checkbox_click1(self, instance, value, selected):
        if value == True:
            FirstWindow.type = selected
        else:
            FirstWindow.type = ""
        print(FirstWindow.type)


    def startrecord(self):
        rec = recorder.Recorder(channels=2)
        global running
        running = None
        tonic = FirstWindow.tonic
        type = FirstWindow.type
        folder_name = type+'_'+str(tonic)
        name=type+'_'+str(tonic)+'.wav'
        if running is not None:
            print('already running')
        else:
            running = rec.open(name, 'wb')
            running.start_recording()

    def stoprecord(self):
        global running
        tonic = FirstWindow.tonic
        type = FirstWindow.type
        folder_name = type+'_'+str(tonic)
        name=type+'_'+str(tonic)+'.wav'
        if running is not None:
            running.stop_recording()
            running.close()
            running = None
        else:
            print('not running')
        if (os.path.exists(f'AudioRecord/{name}')):
            os.remove(f'AudioRecord/{name}')
        os.rename(name, f'AudioRecord/{name}')

    def saverecord(self):
        tonic = FirstWindow.tonic
        type = FirstWindow.type
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
            # plt.title('Power Spectrum ' + f"Pitch = {pitch} Hz")
            return [midBand,highBand]

        def plot_power_spectrum(path,voice,i):
            X = np.fft.fft(voice)
            X_mag = np.absolute(X)
            power_spectrum = np.square(X_mag)
            f = np.linspace(0, sr, len(power_spectrum))
            f_bins=limitFreq(f,2000)
            pitch=round(pitchEstimator(path))
            Pitch.append(pitch)
            plt.subplot(3,6,i)
            plt.plot(f[1:f_bins], power_spectrum[1:f_bins])
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Power')
            plt.title('Power Spectrum ' + f"Pitch = {pitch} Hz")

        # PLOTTING POWER SPECTRUM AND SAVING THEM.
        plt.figure(figsize=(25, 15))
        for j in range(len(sar)):
            plot_power_spectrum(sar[j],voice[j],j+1)
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)
        plt.savefig('pow'+folder_name)
        plt.clf()

        # FINDING MIDBAND & HIGHBAND
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

        # DUMPING VALUES TO JSON
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

        # PLOTTING TRISTIMULUS DIAGRAM
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
        plt.savefig('tri'+folder_name)
        plt.clf()


# SECOND WINDOW - PROGRAM OPTIONS
class SecondWindow(Screen):
    pass


# THIRD WINDOW - ANALYSE TONIC NOTE AND RANGE
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

        self.ids.tonicrange.text = f'{tonic_range1} Hz - {tonic_range2} Hz'
        self.ids.lowestnote.text = f'{lowest_note} Hz'
        self.ids.highestnote.text = f'{highest_note} Hz'

        keys = list(keyboard_keys.keys())
        closest_key = keys[min(range(len(keys)), key = lambda i: abs(keys[i]-tonic_range1))]

        self.ids.closestkey.text = f'{closest_key} Hz'
        self.ids.keyboardkey.text = f'{keyboard_keys[closest_key]}'


# FOURTH WINDOW - FEATURES OPTIONS
class FourthWindow(Screen):
    pass

# FIFTH WINDOW - VIEW TRISTIMULUS DIAGRAM
class FifthWindow(Screen):
    # filename = ObjectProperty()
    tristimulus = ObjectProperty()
    tonic = ""
    type = ""
    def checkbox_click(self, instance, value, selected):
        if value == True:
             FifthWindow.tonic = selected
        else:
            FifthWindow.tonic = ""

        print(FifthWindow.tonic)

    def checkbox_click1(self, instance, value, selected):
        if value == True:
            FifthWindow.type = selected
        else:
            FifthWindow.type = ""
        print(FifthWindow.type)

    def view(self):
        name = FifthWindow.type+FifthWindow.tonic
        if name:
            self.ids.tristimulus.source = 'tri' + name+'.png'

# SIXTH WINDOW - VIEW POWER SPRECTRUM DIAGRAM
class SixthWindow(Screen):
    # filename = ObjectProperty()
    power = ObjectProperty()
    tonic = ""
    type = ""
    def checkbox_click(self, instance, value, selected):
        if value == True:
             SixthWindow.tonic = selected
        else:
            SixthWindow.tonic = ""

        print(SixthWindow.tonic)

    def checkbox_click1(self, instance, value, selected):
        if value == True:
            SixthWindow.type = selected
        else:
            SixthWindow.type = ""
        print(SixthWindow.type)

    def view(self):
        name = SixthWindow.type+SixthWindow.tonic
        if name:
            self.ids.power.source = 'pow'+name+'.png'

# SEVENTH WINDOW - TIME DOMAIN FEATURE ANALYSIS
class SeventhWindow(Screen):
    tonic = ""
    type = ""
    def checkbox_click(self, instance, value, selected):
        if value == True:
             SeventhWindow.tonic = selected
        else:
            SeventhWindow.tonic = ""

        print(SeventhWindow.tonic)

    def checkbox_click1(self, instance, value, selected):
        if value == True:
            SeventhWindow.type = selected
        else:
            SeventhWindow.type = ""
        print(SeventhWindow.type)

    def timedomain(self):
        BASE_FOLDER = "./AudioFiles"
        sound_file = SeventhWindow.type +'_' +SeventhWindow.tonic + '.wav'

        # load sounds
        voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))
        frame_length = 1024
        hop_length = 512

        # Zcr
        zcr = librosa.feature.zero_crossing_rate(voice, frame_length=frame_length, hop_length=hop_length, center=True)[0]
        mean_zcr = format(np.mean(zcr), '.3f')
        frames = range(len(zcr))
        t = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)
        librosa.display.waveshow(voice, alpha=0.5)
        plt.figure(figsize=(25, 5))
        plt.plot(t, zcr, color="black")
        plt.title("ZCR")
        plt.savefig("zcr")
        plt.clf()

        # RMSE
        rmse = librosa.feature.rms(voice, frame_length=frame_length, hop_length=hop_length, center=True)[0]
        mean_rmse = format(np.mean(rmse), '.3f')
        frames = range(len(rmse))
        t = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)
        plt.plot(t, rmse, color="black")
        plt.title("RMSE")
        plt.savefig("rmse")
        plt.clf()

        # Beats Per Minute
        # Tempogram
        onset_env = librosa.onset.onset_strength(voice, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=hop_length)
        librosa.display.specshow(tempogram,sr=sr, hop_length=hop_length,x_axis='time', y_axis='tempo')
        plt.axhline(tempo, color='w', linestyle='--', alpha=1,label='Estimated tempo={:g}'.format(tempo))
        plt.title("Tempogram")
        tempo = format(tempo,'.3f')
        plt.savefig('tempo')
        plt.clf()

        # Harmonic & Percussive Signals
        y_harmonic, y_percussive = librosa.effects.hpss(voice)
        plt.figure(figsize=(15, 5))
        librosa.display.waveshow(y_harmonic, sr=sr, alpha=0.25)
        librosa.display.waveshow(y_percussive, sr=sr, color='red', alpha=0.5)
        plt.title('Harmonic + Percussive')
        plt.savefig('hpsignal')
        plt. clf()

        self.ids.mean_zcr.text = f'{mean_zcr}'
        self.ids.mean_rmse.text = f'{mean_rmse}'
        self.ids.tempo.text = f'{tempo} Beats/min'

# VIEW ZCR
class TenthWindow(Screen):
    def on_enter(self):
        self.ids.zcr_source.source = 'zcr.png'

# class EleventhWindow(Screen):
#     pass

# VIEW RMSE
class TwelvethWindow(Screen):
    def on_enter(self):
        self.ids.rmse_source.source = 'rmse.png'

# VIEW TEMPO
class ThirteenthWindow(Screen):
    def on_enter(self):
        self.ids.tempo_source.source = 'tempo.png'

# VIEW HARMONIC & PERCUSSIVE SIGNALS
class FourteenthWindow(Screen):
    def on_enter(self):
        self.ids.hpsignal_source.source = 'hpsignal.png'

# EIGHTH WINDOW - FREQUENCY DOMAIN ANALYSIS
class EighthWindow(Screen):
    tonic = ""
    type = ""
    def checkbox_click(self, instance, value, selected):
        if value == True:
             EighthWindow.tonic = selected
        else:
            EighthWindow.tonic = ""

        print(EighthWindow.tonic)

    def checkbox_click1(self, instance, value, selected):
        if value == True:
            EighthWindow.type = selected
        else:
            EighthWindow.type = ""
        print(EighthWindow.type)

    def frequencydomain(self):

        def normalize(x, axis=0):
            return sklearn.preprocessing.minmax_scale(x, axis=axis)

        BASE_FOLDER = "./AudioFiles"
        sound_file = EighthWindow.type +'_'+ EighthWindow.tonic + '.wav'

        # load sounds
        voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))
        frame_length = 1024
        hop_length = 512

        spectral_centroids = librosa.feature.spectral_centroid(voice, sr=sr, n_fft=frame_length, hop_length=hop_length)[0]
        mean_spectral_centroids = format(np.mean(spectral_centroids),'.3f')

        spectral_bandwidth = librosa.feature.spectral_bandwidth(voice, sr = sr, n_fft=frame_length, hop_length=hop_length)[0]
        mean_spectral_bandwidth = format(np.mean(spectral_bandwidth),'.3f')

        spectral_rolloff = librosa.feature.spectral_rolloff(voice, sr = sr, n_fft=frame_length, hop_length=hop_length)[0]
        mean_spectral_rolloff = format(np.mean(spectral_rolloff), '.3f')

        spectral_flux = librosa.onset.onset_strength(voice, sr=sr)
        mean_spectral_flux = format(np.mean(spectral_flux), '.3f')

        spectral_contrast=librosa.feature.spectral_contrast(voice,sr=sr, n_fft=frame_length, hop_length=hop_length)[0]
        mean_spectral_contrast = format(np.mean(spectral_contrast), '.3f')

        frames = range(len(spectral_centroids))
        f_times = librosa.frames_to_time(frames, hop_length=hop_length)
        plt.figure(figsize=(20,5))
        librosa.display.waveshow(voice, sr=sr, alpha=0.4)
        plt.plot(f_times, normalize(spectral_centroids), color='black', label='spectral centroids')
        plt.xlabel('Time')
        plt.title("Spectral Centroid")
        plt.savefig('centroid')
        plt.clf()

        plt.figure(figsize=(20,5))
        librosa.display.waveshow(voice, sr=sr, alpha=0.4)
        plt.plot(f_times, normalize(spectral_bandwidth), color='black', label='spectral bandwidth')
        plt.xlabel('Time')
        plt.title("Spectral Bandwidth")
        plt.savefig('bandwidth')
        plt.clf()

        plt.figure(figsize=(20,5))
        librosa.display.waveshow(voice, sr=sr, alpha=0.4)
        plt.plot(f_times, normalize(spectral_rolloff), color='black', label='spectral rolloff')
        plt.xlabel('Time')
        plt.title("Spectral rolloff")
        plt.savefig('rolloff')
        plt.clf()

        plt.figure(figsize=(20,5))
        librosa.display.waveshow(voice, sr=sr, alpha=0.4)
        plt.plot(f_times, normalize(spectral_flux), color='black', label='spectral flux')
        plt.xlabel('Time')
        plt.title("Spectral flux")
        plt.savefig('flux')
        plt.clf()

        plt.figure(figsize=(20,5))
        librosa.display.waveshow(voice, sr=sr, alpha=0.4)
        plt.plot(f_times, normalize(spectral_contrast), color='black', label='spectral flux')
        plt.xlabel('Time')
        plt.title("Spectral Contrast")
        plt.savefig('contrast')
        plt.clf()

        self.ids.centroid.text = f'{mean_spectral_centroids}'
        self.ids.bandwidth.text = f'{mean_spectral_bandwidth}'
        self.ids.rolloff.text = f'{mean_spectral_rolloff}'
        self.ids.flux.text = f'{mean_spectral_flux}'
        self.ids.contrast.text = f'{mean_spectral_contrast}'

# VIEW SPECTRAL CENTROID
class FifteenthWindow(Screen):
    def on_enter(self):
        self.ids.centroid_source.source = 'centroid.png'

# VIEW SPECTRAL BANDWIDTH
class SixteenthWindow(Screen):
    def on_enter(self):
        self.ids.bandwidth_source.source = 'bandwidth.png'

# VIEW SPECTRAL ROLLOFF
class SeventeenthWindow(Screen):
    def on_enter(self):
        self.ids.rolloff_source.source = 'rolloff.png'

# VIEW SPECTRAL FLUX
class EighteenthWindow(Screen):
    def on_enter(self):
        self.ids.flux_source.source = 'flux.png'

# VIEW SPECTRAL CONTRAST
class NineteenthWindow(Screen):
    def on_enter(self):
        self.ids.contrast_source.source = 'contrast.png'

# EIGHTH WINDOW - TIME-FREQUENCY DOMAIN ANALYSIS
class NinethWindow(Screen):
    tonic = ""
    type = ""
    def checkbox_click(self, instance, value, selected):
        if value == True:
             NinethWindow.tonic = selected
        else:
            NinethWindow.tonic = ""

        print(NinethWindow.tonic)

    def checkbox_click1(self, instance, value, selected):
        if value == True:
            NinethWindow.type = selected
        else:
            NinethWindow.type = ""
        print(NinethWindow.type)

    def timefrequencydomain(self):

        BASE_FOLDER = "./AudioFiles"
        sound_file = NinethWindow.type +'_' + NinethWindow.tonic + '.wav'
        # load sounds

        voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))
        frame_length = 1024
        hop_length = 512
        number_of_mfcc = 13

        y_harmonic, y_percussive = librosa.effects.hpss(voice)

        d_audio = np.abs(librosa.stft(voice, n_fft=frame_length, hop_length=hop_length))
        db_audio = librosa.amplitude_to_db(d_audio, ref=np.max)
        spectrogram = format(np.mean(db_audio[0]),'.3f')

        plt.figure(figsize=(20, 5))
        librosa.display.specshow(db_audio, sr=sr, hop_length=hop_length, x_axis="time", y_axis="linear")
        plt.colorbar(format="%+2.f")
        plt.savefig('spectrogram')
        plt.clf()

        s_audio = librosa.feature.melspectrogram(voice, sr=sr)
        s_db_audio = librosa.amplitude_to_db(s_audio, ref=np.max)
        mel_spectrogram = format(np.mean(s_db_audio[0]),'.3f')

        plt.figure(figsize=(25, 5))
        librosa.display.specshow(s_db_audio, x_axis="time",y_axis="mel", sr=sr)
        plt.colorbar(format="%+2.f")
        plt.savefig('mel')
        plt.clf()

        mfccs = librosa.feature.mfcc(voice, sr=sr, n_mfcc=number_of_mfcc)
        plt.figure(figsize=(25, 5))
        librosa.display.specshow(mfccs, sr=sr, x_axis='time')
        plt.colorbar(format="%+2.f")
        plt.savefig('mfcc')
        plt.clf()

        chroma = librosa.feature.chroma_cens(y=y_harmonic, sr=sr)
        plt.figure(figsize=(25, 5))
        librosa.display.specshow(chroma,y_axis='chroma', x_axis='time')
        plt.colorbar()
        plt.savefig('chroma')
        plt.clf()

        chroma_mean = np.mean(chroma,axis=1)
        chroma_std = np.std(chroma,axis=1)
        octave = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        plt.figure(figsize = (25,5))
        plt.title('Mean CENS')
        sns.barplot(x=octave,y=chroma_mean)
        plt.savefig('pitchhistogram')
        plt.clf()

        # mfcc_features = []
        # for i in range(0, number_of_mfcc):
        #     mfcc_value = np.mean(mfccs[i])
        #     mfcc_features.append(mfcc_value)

        self.ids.spectrogram.text = f'{spectrogram}'
        self.ids.melspectrogram.text = f'{mel_spectrogram}'
        # self.ids.mfcc.text = f'{mfcc_features}'
        # self.ids.chromafeatures.text = f'{mean_spectral_flux}'

# VIEW SPECTROGRAM
class TwentythWindow(Screen):
    def on_enter(self):
        self.ids.spectrogram_source.source = 'spectrogram.png'

# VIEW MEL-SPECTROGRAM
class TwentyfirstWindow(Screen):
    def on_enter(self):
        self.ids.mel_source.source = 'mel.png'

# VIEW MFCC
class TwentysecondWindow(Screen):
    def on_enter(self):
        self.ids.mfcc_source.source = 'mfcc.png'

# VIEW CHROMA FEATURES
class TwentythirdWindow(Screen):
    def on_enter(self):
        self.ids.chroma_source.source = 'chroma.png'

# VIEW PITCH HISTOGRAM
class TwentyfourthWindow(Screen):
    def on_enter(self):
        self.ids.pitchhistogram_source.source = 'pitchhistogram.png'

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('voiceanalysis.kv')

class VoiceApp(App):

    def build(self):
        running = None
        return kv

if __name__=='__main__':
    VoiceApp().run()
