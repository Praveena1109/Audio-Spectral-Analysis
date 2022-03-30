import os

def get_pitches(audioFile: str):
    pitches = []
    stream = os.popen('aubio pitch {}'.format(audioFile))
    outputs = stream.readlines()
    for line in outputs:
        pitches.append(float(line.rstrip().split("\t")[1]))
    return pitches


def compare_pitches(a: list, b: list):
    sum = 0
    for i in range(len(a)):
        # Prevents dividing by zero
        if(a[i] == 0):
            continue
        if(i >= len(b)):
            break
        # Percentage difference between the i'th element in a and b
        actual_pitch = a[i]
        user_pitch = b[i]
        if(abs(actual_pitch - user_pitch) <= 50):
            sum += 1
    sum /= len(a)
    sum *= 100
    return sum


def main():

    user_file = "./Kodaline-All-I-Want_Vocals.wav"
    bot_file = "./Kodaline-All-I-Want_Vocals.wav"

    user_pitches = get_pitches(user_file)
    song_pitches = get_pitches(bot_file)

    pitches_diff = compare_pitches(song_pitches, user_pitches)

    output = {'score': '{}'.format(pitches_diff)}

    print(output)
    return pitches_diff

main()
