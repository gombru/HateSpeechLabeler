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


def get_data2label():
    base_path = '../../datasets/HateSPic/HateSPicLabeler/filtered_original_json/'
    datasets = ['HateSPic','SemiSupervised','DT','RM','WZ-LS']

    data2label = []

    for dataset in datasets:
        c=0
        for filename in glob.glob(base_path + dataset + '/' + '*.json'):
            with open(filename) as data:
                data2label.append(json.load(data))
                c+=1

        print "Loaded: " + dataset + ". Dataset elements: " + str(c)

    print "All loaded. Elements: " + str(len(data2label))
    random.shuffle(data2label)

    return data2label