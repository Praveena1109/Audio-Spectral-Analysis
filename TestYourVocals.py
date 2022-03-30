from tkinter.tix import Select
import pyaudio
import wave
import time

# print("Enter your name: ")
# name = input()
# list_of_Songs = ["Kodaline - All I Want"]
# for i,j in enumerate(list_of_Songs):
#     print(i,j)
# print("Select one song")
# song_no = int(input())
# lyrics = ["All I want is nothing more To hear you knocking at my door Cause if I could see your face once more I could die as a happy man I'm sure When you said your last goodbye died a little bit inside I lay in tears in bed all night Alone without you by my side But if you loved me Why did you leave me Take my body Take my body All I want is All I need is To find somebody I'll find somebody Ooh oh Ooh oh Ooh oh Ooh oh Cause you brought out the best of me A part of me I'd never seen You took my soul wiped it clean Our love was made for movie screens But if you loved me Why did you leave me Take my body Take my body All I want is All I need is To find somebody I'll find somebody Ooh oh Ooh oh Ooh oh Ooh oh Ooh ah Ooh oh Ooh, if you loved me Why did you leave me Take my body Take my body All I want is All I need is To find somebody I'll find somebody Like you, ooh"]
# # print(lyrics[song_no])

ORIGINAL_FILE = "./Kodaline-All-I-Want_Vocals.wav"

# audio = pyaudio.PyAudio()
# stream = audio.open(format = pyaudio.paInt16, channels=1, rate = 44100, input=True, frames_per_buffer=1024)
# print("Recording started for 30 secs")
# frames = []
# timeout = 30 # [seconds]
# timeout_start = time.time()
# while time.time() < timeout_start + timeout:
#     data = stream.read(60)
#     frames.append(data)

# stream.stop_stream()
# stream.close()
# audio.terminate()

# print("Finished Recording")

# sound_file = wave.open(name+".wav","wb")
# sound_file.setnchannels(1)
# sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
# sound_file.setframerate(44100)
# sound_file.writeframes(b''.join(frames))
# sound_file.close()

MISSING_PITCH_PLACEHOLDER = 0
RECORD_SECONDS = 30

def calculateScore(audio_file_one, audio_file_two):
    file_one_pitches = getPitch(audio_file_one)
    file_two_pitches = getPitch(audio_file_two)
    score = min(100, round(pitchAlgorithm(file_one_pitches, file_two_pitches)))
    return score

def getPitch(filename):
    from aubio import pitch, source
    # buffer size (window size) - higher is good for lower frequencies
    win_s = 4096
    hop_s = 512
    s = source(filename)  # wav samplerate is 44.1kH
    tolerance = 0.8
    pitch_o = pitch("yin", win_s)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)
    pitches, confidences = [], []
    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitch = round(pitch, 3)
        confidence = pitch_o.get_confidence()
        if confidence < 0.60:
            pitch = 0
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s:
            break
    return pitches

def convertPitchesToNotes(pitches):
    pitchDict = makePitchMap()
    notes = []
    for pitch in pitches:
        rounded_pitch = int(round(pitch))
        if rounded_pitch in pitchDict:
            notes += [pitchDict[rounded_pitch]]
        else:
            notes += [MISSING_PITCH_PLACEHOLDER]
    return notes

def makePitchMap():
    dictionary = {}
    for i in range(0, 7):
        key = 24 + i*12
        dictionary[key] = 'C' + str(i + 1)

        key = 25 + i*12
        dictionary[key] = 'C#' + str(i + 1)

        key = 26 + i*12
        dictionary[key] = 'D' + str(i + 1)

        key = 27 + i*12
        dictionary[key] = 'D#' + str(i + 1)

        key = 28 + i*12
        dictionary[key] = 'E' + str(i + 1)

        key = 29 + i*12
        dictionary[key] = 'F' + str(i + 1)

        key = 30 + i*12
        dictionary[key] = 'F#' + str(i + 1)

        key = 31 + i*12
        dictionary[key] = 'G' + str(i + 1)

        key = 32 + i*12
        dictionary[key] = 'G#' + str(i + 1)

        key = 33 + i*12
        dictionary[key] = 'A' + str(i + 1)

        key = 34 + i*12
        dictionary[key] = 'A#' + str(i + 1)

        key = 35 + i*12
        dictionary[key] = 'B' + str(i + 1)

    dictionary[108] = 'C8'

    return dictionary

def pitchAlgorithm(userPitches, realPitches):
    interval = round(len(realPitches)/(RECORD_SECONDS*4))
    userPitches = reduceWhiteNoise(userPitches, realPitches)
    # concatenate extra frames
    begin, end = 0, 0
    for i in range(len(userPitches) - 1):
        if int(userPitches[i]) == 0 and int(userPitches[i+1] != 0):
            begin = i + 1
            break
    for j in range(len(userPitches) - 1, begin, -1):
        if int(userPitches[j-1]) != 0 and int(userPitches[j]) == 0:
            end = j
            break
    userPitches = userPitches[begin:end]
    realPitches = realPitches[begin:end]
    userNotes = convertPitchesToNotes(userPitches)
    realNotes = convertPitchesToNotes(realPitches)
    score = 0
    total = min(len(userNotes), len(realNotes))

    for i in range(0, len(realNotes)-interval, interval):
        for j in range(-1*interval//2, interval//2, 1):
            if realNotes[i+j] == 0 or userNotes[i+j] == 0:
                score += 1
            elif (compareNotes(realNotes[i], userNotes[i+j])):
                score += 1
    return (score/max(1,total))*100

def compareNotes(A, B):
    return A == B

def reduceWhiteNoise(userArray, realArray):
    # 20 samples per second
    interval = 10
    # beginning case
    if (userArray[:5] != [0]*5):
        userArray[0] = 0
    # end case
    if (userArray[-5:] != [0]*5):
        userArray[-1] = 0
    for i in range(len(userArray)-interval):
        if (userArray[i:i+interval//2-1] == [0]*(interval//2-1) and userArray[i+interval//2+1: i+interval] == [0]*(interval//2-1)):
            if userArray[i+interval//2-1:i+interval//2+1] != realArray[i+interval//2-1:i+interval//2+1]:
                userArray[i+interval//2-1] = 0
                userArray[i+interval//2] = 0
    return userArray

score = calculateScore("./Kodaline-All-I-Want_Vocals.wav", "./Kodaline-All-I-Want_Vocals.wav")
print(score)
