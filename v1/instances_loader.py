# Reads the json of each element to be labeled and returns them in an array of dicts
# The dict format is:
# info = {}
# info['id'] = t['id']
# info['img_url'] = t['entities']['media'][0]['media_url']
# info['text'] = t['text'].encode("utf8", "ignore").replace('\n', ' ').replace('\r', ' ')
# info['dataset'] = dataset_name
# info['hate_votes'] = None
# info['not_hate_votes'] = None
# info['voters'] = None
# info['HateSPiclabeler_annotation'] = None
# info['original_annotation'] = label_id
# The file is named 'id.json'

import glob
import json
import random
import requests
import urllib
from PIL import Image

# review_words = ['redneck','white','whitetrash','neck']


def download_save_image(url, image_path):
    resource = urllib.urlopen(url)
    output = open(image_path, "wb")
    output.write(resource.read())
    output.close()

def get_data2label():
    base_path = '../../datasets/HateSPic/HateSPicLabeler/filtered_original_json/'
    # datasets = ['HateSPic','SemiSupervised','DT','RM','WZ-LS']
    datasets = ['HateSPic']

    # Load all already annotated files
    annotated_path = '../../datasets/HateSPic/HateSPicLabeler/generated_json/'
    discarded_path = '../../datasets/HateSPic/HateSPicLabeler/discarded_json/'
    already_annotated = []
    for dataset in datasets:
        for filename in glob.glob(annotated_path + dataset + '/' + '*.json'):
            already_annotated.append(filename.split('/')[-1].split('.')[0])
        for filename in glob.glob(discarded_path + dataset + '/' + '*.json'):
            already_annotated.append(filename.split('/')[-1].split('.')[0])

    print("Already annotated (and discarded) files: " + str(len(already_annotated)))

    data2label = []

    for dataset in datasets:
        c=0
        total=0
        for filename in glob.glob(base_path + dataset + '/' + '*.json'):

            # Check that the tweet has not been annotated yet
            if filename.split('/')[-1].split('.')[0] in already_annotated: continue

            with open(filename) as data:
                info = json.load(data)

                # if 'trump' in info['text'].lower(): continue
                # for w in review_words:
                #     if w in info['text'].lower():

                # Select deleted tweets
                try:
                    download_save_image(info['img_url'], "/home/raulgomez/datasets/img_test.jpg")
                    im = Image.open("/home/raulgomez/datasets/img_test.jpg")
                    print(str(c) + " out of " + str(total))
                    total+=1
                except:
                    # print "Failed downloading image"
                    data2label.append(info)
                    c += 1
                    print c
                    continue

                # data2label.append(info)
                # c+=1
                # if c == 5: break

        print "Loaded: " + dataset + ". Dataset elements: " + str(c)

    print "All loaded. Elements: " + str(len(data2label))
    random.shuffle(data2label)

    return data2label