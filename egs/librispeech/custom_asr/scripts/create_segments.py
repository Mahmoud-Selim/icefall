import sys
import shutil
import argparse
import os
import lhotse
import sox 

class SegmentsMaker():
    def __init__(self, scp_file, output_file):
        self.scp_file = scp_file
        self.output_file = output_file


    def make_segments_file(self):
        segments_fh = open(self.output_file, "w")

        scp_fh = open(self.scp_file)

        for line in scp_fh:
            wav_id, wav_path = line.strip().split()
            start, end = 0, sox.file_info.duration(wav_path)

            segments_fh.write(wav_id + " " + wav_id + " " + str(start) + " " + str(end) + "\n")

        segments_fh.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--scp-file', help='path to wav.scp file using kaldi style')
    parser.add_argument('--output-file', help='path to segments output file')
    args = parser.parse_args()
    SM = SegmentsMaker(args.scp_file, args.output_file)
    SM.make_segments_file()
