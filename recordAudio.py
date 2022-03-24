from tkinter.tix import Select
import pyaudio
import wave
import time

print("Enter your name: ")
name = input()

audio = pyaudio.PyAudio()
stream = audio.open(format = pyaudio.paInt16, channels=1, rate = 44100, input=True, frames_per_buffer=1024)
print("Recording started for 15 secs")
frames = []
timeout = 15  # [seconds]
timeout_start = time.time()
while time.time() < timeout_start + timeout:
    data = stream.read(1024)
    frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()

print("Finished Recording")

sound_file = wave.open(name+".wav","wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b''.join(frames))
sound_file.close()

