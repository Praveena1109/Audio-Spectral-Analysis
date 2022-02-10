import crepe
from scipy.io import wavfile
sr, audio = wavfile.read('adish_alap_aroh_b1.wav')
# print(audio.size)
# print(sr)
time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True)
