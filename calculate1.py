import json
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

print("Tonic Range: ", tonic_range1,"Hz","-", tonic_range2,"Hz")
print("Lowest Note: ",lowest_note,"Hz" )
print("Highest Note: ",highest_note,"Hz")
# print(highest_note,lowest_note,tonic_range1,tonic_range2)
keys = list(keyboard_keys.keys())
closest_key = keys[min(range(len(keys)), key = lambda i: abs(keys[i]-tonic_range1))]
print("Closest Key Frequency: ",closest_key,"Hz" )
print("Keyboard Key: ",keyboard_keys[closest_key])
