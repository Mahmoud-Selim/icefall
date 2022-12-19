import glob
import lhotse
from io import StringIO
import sys
from lhotse import CutSet
import json 

supervisions = glob.glob("data/colloquial_arabic/*supervisions*.jsonl")
recordings = glob.glob("data/colloquial_arabic/*recordings*.jsonl")


output = dict()
#xx = CutSet.from_manifests(recordings=x)
for recording in recordings:
    recording_data = dict()
    data = lhotse.load_manifest(recording)
    data = CutSet.from_manifests(recordings=data)
    buffer = StringIO()
    sys.stdout = buffer
    data.describe()
    sys.stdout = sys.__stdout__
    y = buffer.getvalue()

    stats = y.strip().replace("\n***", "").split("\n")
    for stat in stats:
        if(stat.find(":") > 0):
            #print(stat.split(":")[1])
            recording_data[stat.split(":")[0]] = stat.split(":")[1]
        else:
            recording_data[stat.split("\t")[0]] = stat.split("\t")[1]
            #print(stat.split("\t")[1])

    output[recording] = recording_data


with open('result.json', 'w') as fp:
    json.dump(output, fp)
