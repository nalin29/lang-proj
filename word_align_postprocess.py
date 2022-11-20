import textgrid
import os

textgrid_folder = "flickr_corpus_aligned"

outputName = "raw_ali.txt"
output = open(outputName, "w")

num = 0
for folder in os.listdir(textgrid_folder):
    folderPath = os.path.join(textgrid_folder, folder)
    if os.path.isfile(folderPath):
        continue
    
    for textgrid_name in os.listdir(folderPath):
        textgrid_path = os.path.join(folderPath, textgrid_name)
        filename = textgrid_name.split('.')[0]

        tg = textgrid.TextGrid.fromFile(textgrid_path)

        intervals = []
        for interval in tg[0]:
            if interval.mark == "":
                continue
            intervals.append(f"{interval.minTime}__{interval.mark}__{interval.maxTime}")
        intervals = " ".join(intervals)
        
        output.write(f"{filename}\t{intervals}\n")

        num += 1
        print(f"\rFinished {num} files", end="")

output.close()