from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

path = "Sargam/adish_sargam_avaroh_b1.wav"
name='Adish_avaroh_b1'
dirName = f'TestSargam/{name}'
try:
    # Create target Directory
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

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
    silence_thresh = -30
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
        print("Exporting sar0{0}.wav to {1}".format(i,name))
        normalized_chunk.export(
        "./{1}/sar0{0}.wav".format(i,dirName),
        bitrate = "192k",
        format = "wav"
    )
    else:
        print("Exporting sar{0}.wav to {1}".format(i,name))
        normalized_chunk.export(
        "./{1}/sar{0}.wav".format(i,dirName),
        bitrate = "192k",
        format = "wav"
    ) 


for filename in sorted(os.listdir(dirName)):
    f = os.path.join(dirName, filename)
    # print(f)  
    if os.path.getsize(f) < 40*1024:
        os.remove(f)
        print

count=1
for filename in sorted(os.listdir(dirName)):
    
    old = os.path.join(dirName, filename)
    new=f[:27]+f'Sargam{count}.wav'  
    os.rename(old,new)
    # print(old,new)
    count+=1
    