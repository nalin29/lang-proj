import shutil
import os

wav_path = os.path.join("flickr_data", "wavs")
image_to_cap_file = os.path.join("flickr_data", "Flickr8k.token.txt")
wav_to_spkr_file = os.path.join("flickr_data", "wav2spk.txt")

outputDir = "flickr_corpus"
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

# get speakers
file_to_spkr = {}
spkrs = set()
with open(wav_to_spkr_file) as f:
    for line in f.readlines():
        line = line.split()
        file_to_spkr[line[0].split('.')[0]] = line[1]
        spkrs.add(line[1])

# create directories for each speaker
for s in spkrs:
    speakerDir = os.path.join(outputDir, f"speaker{s}")
    if not os.path.exists(speakerDir):
        os.mkdir(speakerDir)

# copy wav files into speaker directories
num = 0
for filename in file_to_spkr:
    s = file_to_spkr[filename]
    speakerDir = os.path.join(outputDir, f"speaker{s}")
    filename = f"{filename}.wav"

    wavFileOrig = os.path.join(wav_path, filename)
    # print(wavFileOrig)
    # print(speakerDir)
    shutil.copy2(wavFileOrig, speakerDir)

    num += 1
    print(f"\rCopied {num} of {len(file_to_spkr)} wav files", end="")

# add captions to speaker directories
num = 0
with open(image_to_cap_file) as f:
    for line in f.readlines():
        line = line.split("\t")
        splitFilename = line[0].split("#")
        prefix = splitFilename[0].split(".")[0]
        suffix = splitFilename[1]
        filename = f"{prefix}_{suffix}"
        caption = line[1]

        # get speaker dir
        if filename not in file_to_spkr:
            continue
        s = file_to_spkr[filename]
        speakerDir = os.path.join(outputDir, f"speaker{s}")
        
        # create caption file
        capFileName = os.path.join(speakerDir, f"{filename}.lab")
        # print(capFileName)
        # print(caption)
        capFile = open(capFileName, "w")
        capFile.write(caption)
        capFile.close()

        num += 1
        print(f"\rCreated {num} of {len(file_to_spkr)} caption files", end="")
