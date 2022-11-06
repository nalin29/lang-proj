import json
import os

base_path = os.getcwd()
image_path = os.path.join(base_path, "flickr_data/images/")
wav_path = os.path.join(base_path, "flickr_data/wavs/")
wav_to_cap_file = os.path.join(base_path, "flickr_data/wav2capt.txt")
image_to_cap_file = os.path.join(base_path, "flickr_data/Flickr8k.token.txt")
wav_to_spkr_file = os.path.join(base_path, "flickr_data/wav2spk.txt")


data_json = dict()
data = []

data_json['image_base_path'] = image_path
data_json['audio_base_path'] = wav_path

wav_to_spkr = dict()
with open(wav_to_spkr_file) as f:
    for line in f.readlines():
        line = line.split(maxsplit=1)
        wav_to_spkr[line[0]] = line[1][:-1]
    f.close()

image_to_cap = dict()
with open(image_to_cap_file) as f:
    for line in f.readlines():
        line = line.split(maxsplit=1)
        image_to_cap[line[0]] = line[1]
    f.close()

with open(wav_to_cap_file) as f:
    for line in f.readlines():
        line = line.split()
        wav = line[0]
        image = line[1]
        caption = line[2]
        asr_text_index = image + caption
        datum = {
            "uttid": asr_text_index,
            "speaker": wav_to_spkr[wav],
            "asr_text": image_to_cap[asr_text_index],
            "wav": wav,
            "image": image, 
            "scenelabel": "",
            "text_alignment": "<None>"
        }
        data.append(datum)
    f.close()

data_json["data"] = data

with open("flickr_data.json", "w+") as outfile:
    outfile.write(json.dumps(data_json, indent=4))