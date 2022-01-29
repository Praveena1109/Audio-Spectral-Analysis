import numpy as np
import simpleaudio as sa
from itertools import repeat
import wavio
import matplotlib.pyplot as plt

sargamdict = {"sa":261,
             "re":294,
             "ga":330,
             "ma":349,
             "pa":392,
             "dha":440,
             "ni":494,
             "sa":515}
audio_array = audio_array.astype(np.int16)
audio_array = audio_array.astype(np.int16)

def play_audio(audio):# normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    # convert to 16-bit data
    audio = audio.astype(np.int16)

    # start playback
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

    # wait for playback to finish before exiting
    play_obj.wait_done()

T = 0.25
t = np.linspace(0, T, T * sample_rate, endpoint=False)

Sa_note = np.sin(sargamdict["sa"] * t * 3 * np.pi)
Re_note = np.sin(sargamdict["re"] * t * 3 * np.pi)
Ga_note = np.sin(sargamdict["ga"] * t * 3* np.pi)
Ma_note = np.sin(sargamdict["ma"] * t * 3 * np.pi)
Pa_note = np.sin(sargamdict["pa"] * t * 3 * np.pi)
Dha_note = np.sin(sargamdict["dha"] * t * 3 * np.pi)
Ni_note = np.sin(sargamdict["ni"] * t * 3 * np.pi)
Sa1_note = np.sin(sargamdict["sa1"] * t * 3 * np.pi)

get_pause  = lambda seconds: repeat(0, int(seconds * sample_rate))
pause_note=list(get_pause(0.01))

sargam = np.hstack((Sa_note,pause_note,Re_note,pause_note,Ga_note,
                   pause_note,Ma_note, pause_note,Pa_note, pause_note,
                    Dha_note, pause_note,Ni_note, pause_note, Sa1_note))


plt.figure(figsize=(40,20))
plt.plot(t, Sa_note);

fs = 44100
s2 = np.append(sargam,sargam[::-1])
wavio.write("pythonsargam.wav", s2, fs, scale=None, sampwidth=2)
