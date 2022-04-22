import numpy as np                 # for handling large arrays
import scipy                       # for common math functions
import sklearn                     # a machine learning library
import os                          # for accessing local files
import IPython.display as ipd
import librosa.display             # librosa plot functions
import matplotlib.pyplot as plt    # plotting with Matlab functionality
import seaborn as sns              # data visualization based on matplotlib
import librosa

BASE_FOLDER = "/Users/Praveena Acharya/Desktop/FINAL YEAR BE PROJECT/Audio Spectral Analysis"
sound_file = "Aroh_120.wav"

ipd.Audio(os.path.join(BASE_FOLDER, sound_file))

voice, sr = librosa.load(os.path.join(BASE_FOLDER, sound_file))


# Statistical Features
# freqs = np.fft.fftfreq(voice.size)
# mean = np.mean(freqs)
# std = np.std(freqs)
# maxv = np.amax(freqs)
# minv = np.amin(freqs)
# median = np.median(freqs)
# skew = scipy.stats.skew(freqs)
# kurt = scipy.stats.kurtosis(freqs)
# q1 = np.quantile(freqs, 0.25)
# q3 = np.quantile(freqs, 0.75)
# mode = scipy.stats.mode(freqs)[0][0]
# iqr = scipy.stats.iqr(freqs)
# print(mean, std, maxv, minv, median, skew, kurt, q1, q3, mode, iqr)

# Zero Crossing Rate
# zero_crossings = sum(librosa.zero_crossings(voice, pad=False))
# print(zero_crossings)

# Energy
# e = np.sum(voice**2)
# print(e)


# Root mean square energy
# rsme = np.sqrt(np.mean(voice**2))
# print(rsme)
# hop_length = 256
# frame_length = 512
# # compute sum of signal square by frame
# energy = np.array([
#     sum(abs(voice[i:i+frame_length]**2))
#     for i in range(0, len(voice), hop_length)
# ])
# energy.shape
# # compute RMSE over frames
# rmse = librosa.feature.rms(voice, frame_length=frame_length, hop_length=hop_length, center=True)
# rmse.shape
# rmse = rmse[0]
# # plot energy and rmse along the waveform
# frames = range(len(energy))
# t = librosa.frames_to_time(frames, sr=sr, hop_length=hop_length)
# plt.figure(figsize=(15, 5))
# librosa.display.waveplot(voice, sr=sr, alpha=0.4)
# plt.plot(t, energy/energy.max(), 'r--')                # normalized for visualization
# plt.plot(t[:len(rmse)], rmse/rmse.max(), color='blue') # normalized for visualization
# plt.legend(('Energy', 'RMSE'))
# plt.show()


# S, phase = librosa.magphase(librosa.stft(voice)) # compute magnitude and phase content
# rms = librosa.feature.rms(S=S) # compute root-mean-square for each frame in magnitude
# plt.figure(figsize=(15, 5))
# plt.subplot(2, 1, 1)
# plt.semilogy(rms.T, label='RMS Energy', color="black")
# plt.xticks([])
# plt.xlim([0, rms.shape[-1]])
# plt.legend()
# plt.subplot(2, 1, 2)
# librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
#                             y_axis='log', x_axis='time')
# plt.title('log power spectrogram')
# plt.show()


# Separation of Harmonic & Percussive Signals
# y_harmonic, y_percussive = librosa.effects.hpss(voice)
# plt.figure(figsize=(15, 5))
# librosa.display.waveplot(y_harmonic, sr=sr, alpha=0.25)
# librosa.display.waveplot(y_percussive, sr=sr, color='red', alpha=0.5)
# plt.title('Harmonic + Percussive')
# plt.show()


# Spectral Features


# spectral_centroids = librosa.feature.spectral_centroid(voice)[0]
# spectral_centroids.shape
# # compute the time variable for visualization
# frames = range(len(spectral_centroids))
# f_times = librosa.frames_to_time(frames)
#
# # an auxiliar function to normalize the spectral centroid for visualization
# def normalize(x, axis=0):
#     return sklearn.preprocessing.minmax_scale(x, axis=axis)
#
# plt.figure(figsize=(15,5))
# plt.subplot(1, 1, 1)
# librosa.display.waveplot(voice, sr=sr, alpha=0.4)
# plt.plot(f_times, normalize(spectral_centroids), color='black', label='spectral centroids')
# plt.ylabel('Hz')
# plt.xticks([])
# plt.legend()
# plt.show()

# spectral_bandwidth=librosa.feature.spectral_bandwidth(voice)[0]

# spectral_contrast=librosa.feature.spectral_contrast(voice,sr=sr)[0]
# plt.figure(figsize=(15,5))
# librosa.display.specshow(spectral_contrast, x_axis='time')
# plt.colorbar()
# plt.ylabel('Frequency bands')
# plt.title('Spectral contrast')
# plt.show() 

# spectral_flatness=librosa.feature.spectral_flatness(voice)[0]

# rolloff=librosa.feature.spectral_rolloff(voice,sr=sr)[0]
# plt.figure(figsize=(15,5))
# plt.semilogy(rolloff.T, label='Roll-off frequency')
# plt.ylabel('Hz')
# plt.xticks([])
# plt.xlim([0, rolloff.shape[-1]])
# plt.legend()
# plt.show()
# rolloff_mean = np.mean(rolloff)
# rolloff_std = np.std(rolloff)
# print('Mean: ' + str(rolloff_mean))
# print('STD: ' + str(rolloff_std))

# print(spectral_centroid)
# print(spectral_bandwidth)
# print(spectral_contrast)
# print(spectral_flatness)
# print(rolloff)


# Mel Frequency Cepstral Coefficients (MFCC)
# mfccs=librosa.feature.mfcc(voice,sr=sr,n_mfcc=13)
# plt.figure(figsize=(15, 5))
# librosa.display.specshow(mfccs, x_axis='time')
# plt.colorbar()
# plt.title('MFCCs')
# plt.show()
# print(mfccs)
# print(len(mfccs))

# # An estimate of the tempo in Beats Per Minute (BPM).
# tempo = librosa.beat.tempo(voice)[0]
# print(tempo)

# Beat Extraction
# tempo, beat_frames = librosa.beat.beat_track(voice, sr=sr)
# print('Detected Tempo: '+ str(tempo) + ' beats/min')
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)
# beat_time_diff = np.ediff1d(beat_times)
# beat_nums = np.arange(1, np.size(beat_times))
# fig, ax = plt.subplots()
# fig.set_size_inches(15, 5)
# ax.set_ylabel("Time difference (s)")
# ax.set_xlabel("Beats")
# g = sns.barplot(beat_nums, beat_time_diff, palette="rocket",ax=ax)
# g = g.set(xticklabels=[])
# plt.show()

# Tempogram
hop_length = 512
# tempogram = librosa.feature.tempogram(voice, sr=sr, hop_length=hop_length)
# plt.figure(figsize=(12,8))
# librosa.display.specshow(tempogram,x_axis='time', y_axis='tempo')
# for i in range(1,14):
#     plt.plot(tempogram[i], label=i)
# plt.legend()
# plt.axhline(tempo, color='w', linestyle='--', alpha=1,label='Estimated tempo={:g}'.format(tempo))
# plt.title("Tempogram")
# plt.show()

# tempogram = librosa.feature.tempogram(voice, sr=sr, hop_length=hop_length)
# tempo = librosa.beat.tempo(voice)[0]
# librosa.display.specshow(tempogram,x_axis='time', y_axis='tempo')

# plt.legend(frameon=True, framealpha=0.75)
# plt.figure(figsize=(12,8))
# plt.title("Tempogram")
# plt.show()

onset_env = librosa.onset.onset_strength(voice, sr=sr)
tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)[0]
tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr, hop_length=hop_length)
librosa.display.specshow(tempogram,sr=sr, hop_length=hop_length,x_axis='time', y_axis='tempo')
plt.axhline(tempo, color='w', linestyle='--', alpha=1,label='Estimated tempo={:g}'.format(tempo))
print(tempo)
# plt.legend()
plt.title("Tempogram")
# plt.show()
plt.savefig('new1')

# Ployfeatures
# poly_features=librosa.feature.poly_features(voice) #order 1 by default
# plt.figure(figsize=(12,8))
# plt.plot(poly_features[0], label="0")
# plt.plot(poly_features[1], label="1")
# plt.legend()
# plt.show()


# using a power spectrum
# chroma_d = librosa.feature.chroma_stft(voice, sr=sr)
# plt.figure(figsize=(15, 4))
# librosa.display.specshow(chroma_d, y_axis='chroma', x_axis='time')
# plt.colorbar()
# plt.title('Power spectrum chromagram')
# plt.tight_layout()
# plt.show()


# using an energy (magnitude) spectrum
# S = np.abs(librosa.stft(voice)) # apply short-time fourier transform
# chroma_e = librosa.feature.chroma_stft(S=S, sr=sr)
# plt.figure(figsize=(15, 4))
# librosa.display.specshow(chroma_e, y_axis='chroma', x_axis='time')
# plt.colorbar()
# plt.title('Energy spectrum chromagram')
# plt.tight_layout()
# plt.show()


# using a pre-computed power spectrogram with a larger frame
# S = np.abs(librosa.stft(voice, n_fft=4096))**2
# chroma_p = librosa.feature.chroma_stft(S=S, sr=sr)
# plt.figure(figsize=(15, 4))
# librosa.display.specshow(chroma_p, y_axis='chroma', x_axis='time')
# plt.colorbar()
# plt.title('Pre-computed power spectrogram with larger frame size')
# plt.tight_layout()
# plt.show()


# chroma energy distribution normalized statistics
# chroma = librosa.feature.chroma_cens(voice, sr=sr)
# plt.figure(figsize=(15, 4))
# librosa.display.specshow(chroma,y_axis='chroma', x_axis='time')
# plt.colorbar()
# plt.show()


# a pitch histogram using CENS
# chroma = librosa.feature.chroma_cens(voice, sr=sr)
# chroma_mean = np.mean(chroma,axis=1)
# chroma_std = np.std(chroma,axis=1)
# octave = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
# plt.figure(figsize = (15,5))
# plt.title('Mean CENS')
# sns.barplot(x=octave,y=chroma_mean)
# plt.figure(figsize = (15,5))
# plt.title('Standard Deviation CENS')
# sns.barplot(x=octave,y=chroma_std)
# plt.show()
