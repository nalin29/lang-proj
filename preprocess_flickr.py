import json
import os
import argparse


def create_json(image_path, wav_path, wav_to_cap_file, image_to_cap_file, wav_to_spkr_file, split, train, dev, test):
    jsons = []
    if not split:
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
        jsons.append(data_json)
    else:
        train_json = dict()
        dev_json = dict()
        test_json = dict()
        train_data = []
        dev_data = []
        test_data = []

        train_json['image_base_path'] = image_path
        train_json['audio_base_path'] = wav_path
        dev_json['image_base_path'] = image_path
        dev_json['audio_base_path'] = wav_path
        test_json['image_base_path'] = image_path
        test_json['audio_base_path'] = wav_path

        train_images = set()
        with open(train) as f:
            for line in f.readlines():
                train_images.add(line[:-1])
            f.close()
        
        dev_images = set()
        with open(dev) as f:
            for line in f.readlines():
                dev_images.add(line[:-1])
            f.close()
        
        test_images = set()
        with open(test) as f:
            for line in f.readlines():
                test_images.add(line[:-1])
            f.close()

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
                image_to_cap[line[0]] = line[1][:-1]
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
                if image in train_images:
                    train_data.append(datum)
                elif image in dev_images:
                    dev_data.append(datum)
                else:
                    test_data.append(datum)
                
            f.close()

        train_json["data"] = train_data
        dev_json["data"] = dev_data
        test_json["data"] = test_data
        jsons.append(train_json)
        jsons.append(dev_json)
        jsons.append(test_json)
    
    return jsons

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('image-dir', type=str, help='path to directory of images')
    parser.add_argument('wav-dir', type=str, help='path to directory of wav files')
    parser.add_argument('wav-to-cap', type=str, help='path to mapping of wav files to associated captions')
    parser.add_argument('image-to-cap', type=str, help='path to mapping of images to associated captions')
    parser.add_argument('wav-to-spkr', type=str, help='path to mapping of wave files to associated speaker')
    parser.add_argument('-s', '--split', type=str, nargs=3, metavar=('TRAIN_FILE', 'DEV_FILE', 'TEST_FILE'), help='uses train/dev/test split provided')
    
    args = parser.parse_args()

    def get_and_del_attr(name):
        val = getattr(args, name)
        delattr(args, name)
        return val

    image_path = get_and_del_attr('image-dir')
    wav_path = get_and_del_attr('wav-dir')
    wav_to_cap_file = get_and_del_attr('wav-to-cap')
    image_to_cap_file = get_and_del_attr('image-to-cap')
    wav_to_spkr_file = get_and_del_attr('wav-to-spkr')
    split = get_and_del_attr('split')
    if split:
        train = split[0]
        dev = split[1]
        test = split[2]
        jsons = create_json(image_path, wav_path, wav_to_cap_file, image_to_cap_file, wav_to_spkr_file, True, train, dev, test)
        with open("flickr_data_train.json", "w+") as train_file:
            train_file.write(json.dumps(jsons[0], indent=4))
        with open("flickr_data_dev.json", "w+") as dev_file:
            dev_file.write(json.dumps(jsons[1], indent=4))
        with open("flickr_data_test.json", "w+") as test_file:
            test_file.write(json.dumps(jsons[2], indent=4))
    else:
        with open("flickr_data.json", "w+") as outfile:
            outfile.write(json.dumps(create_json(image_path, wav_path, wav_to_cap_file, image_to_cap_file, wav_to_spkr_file, False, '', '', '')[0], indent=4))

   