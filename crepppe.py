import crepe
import IPython.display as ipd
from scipy.io import wavfile

def pitchEstimator(path):
    sr, audio = wavfile.read(path)
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True,step_size=100)
    lis=[]
    for i,j in enumerate(confidence): 
        if j > 0.92:
            lis.append(i)
    val=[frequency[i] for i in lis]
    return sum(val)/len(val)

a='./Sargam/sargam0.wav'
pitch=round(pitchEstimator(a))
print(pitch)