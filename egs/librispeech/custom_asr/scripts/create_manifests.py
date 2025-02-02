import sys
import shutil
import argparse
import os
import lhotse
from lhotse.kaldi import load_kaldi_data_dir


class Manifest():
    def __init__(self, kaldi_path, sampling_rate):
        self.kaldi_path = kaldi_path
        self.recording_set, self.supervision_set, _ = load_kaldi_data_dir(kaldi_path, sampling_rate)
        self.dataset_name = args.dataset_name
        self.dataset_type = args.dataset_type

    def export(self, out_dir):
        self.recording_set.to_file(os.path.join(out_dir, self.dataset_name + "_recordings_" + self.dataset_type + ".jsonl"))
        self.supervision_set.to_file(os.path.join(out_dir, self.dataset_name + "_supervisions_"+ self.dataset_type + ".jsonl"))
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--kaldi-dir', help='path data dir (kaldi style)')
    parser.add_argument('--output-dir', help='Directory of output manifests')
    parser.add_argument('--dataset-name', help='Name of the dataset. To be used in naming the manifests.')
    parser.add_argument('--dataset-type', help='Type of the dataset (Train, Test, or Valid). To be used in naming the manifests.')
    args = parser.parse_args()
    manifest = Manifest(args.kaldi_dir, 8000)
    manifest.export(args.output_dir)
