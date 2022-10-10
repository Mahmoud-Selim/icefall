import sys
import shutil
import argparse
import os
import pandas as pd
#import lhotse
#import sox 

class Cleaner():
    def __init__(self, args):
        self.scp_file = args.input_scp
        self.text_file = args.input_text
        self.segs_file = args.input_seg
        self.output_dir = args.output_dir

    def clean_data(self):
        valid_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop "
        invalid_letters_id = []
        invalid_letters_trans = []
        long_text_id = []
        long_text_trans = []
        segments = {}
        segs_fh = open(self.segs_file, "r")
        for line in segs_fh:
            wav_id, _, __, end = line.split()
            segments[wav_id] = int(float(end) + 0.5)

        text_fh = open(self.text_file, "r")
        for line in text_fh:
            # Unknowns are replaced with k
            line = line.strip().replace("<unk>", "k")
            line = line.strip().replace("<fil>", "l")
            line = line.strip().replace("<music>", "m")
            line = line.strip().replace("<overlap>", "n")
            line = line.strip().replace("<laugh>", "o")
            line = line.strip().replace("<noise>", "p")
            if(len(line.split()) >= 3 * segments[line.split()[0]]):
                long_text_id.append(line.split()[0])
                long_text_trans.append(line[line.find(" ") + 1: ])
            for letter in line[line.find(" ")+1:]:
                if(not letter in valid_letters):
                    #print(letter, line)
                    invalid_letters_id.append(line.split()[0])
                    invalid_letters_trans.append(line[line.find(" ") + 1: ])


        old_scp_fh = open(self.scp_file)
        new_scp_fh = open(os.path.join(self.output_dir, "wav.scp"), "w")
        for line in old_scp_fh:
            wav_id, wav_path = line.strip().split()
            if(wav_id not in long_text_id and wav_id not in invalid_letters_id):
                new_scp_fh.write(line)

        new_scp_fh.close()
        old_scp_fh.close()
        text_fh.close()

        df = pd.concat((pd.DataFrame({"Long Text ID": long_text_id}),
                             pd.DataFrame({"Invalid Letters ID": invalid_letters_id})))
        df = pd.concat((df, pd.DataFrame({"Trans": long_text_trans + invalid_letters_trans})), axis=1)
                             
        df.to_csv(os.path.join(self.output_dir, "cleaned.csv"), index = False)
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-scp', help='path to input scp file using kaldi style')
    parser.add_argument('--input-seg', help='path to input segments file using kaldi style')
    parser.add_argument('--input-text', help='path to text file using kaldi style')
    parser.add_argument('--output-dir', help='path to segments output file')
    args = parser.parse_args()
    SM = Cleaner(args)
    SM.clean_data()

