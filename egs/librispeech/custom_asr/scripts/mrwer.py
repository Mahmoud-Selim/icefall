import os
import argparse

def match_files(ref_file, hyp_file, out_dir):
    ref_fh = open(ref_file, "r")
    hyp_fh = open(hyp_file, "r")

    hyp_data = {}
    valid_ids = set()
    for line in hyp_fh:
        id = line.split()[0]
        if(id.find("Alaa") > 0):
            id = line.split()[0][:line.split()[0].find("Alaa")]
        elif(id.find("Omar") > 0):
            id = line.split()[0][:line.split()[0].find("Omar")]
        elif(id.find("Mohamed") > 0):
            id = line.split()[0][:line.split()[0].find("Mohamed")]
        elif(id.find("Ali") > 0):
            id = line.split()[0][:line.split()[0].find("Ali")]
        valid_ids.add(id)
        hyp_data[id] = " ".join(line.split()[1:]).strip().replace('i','j').replace('I','g').replace('E','G').replace('B','G').replace('C','G').replace('*','')

    ref_data = {}
    for line in ref_fh:
        id = line.split()[0]
        if(id.find("Alaa") > 0):
            id = line.split()[0][:line.split()[0].find("Alaa")]
        elif(id.find("Omar") > 0):
            id = line.split()[0][:line.split()[0].find("Omar")]
        elif(id.find("Mohamed") > 0):
            id = line.split()[0][:line.split()[0].find("Mohamed")]
        elif(id.find("Ali") > 0):
            id = line.split()[0][:line.split()[0].find("Ali")]
        if(id in valid_ids):
            ref_data[id] = " ".join(line.split()[1:]).strip().replace('i','j').replace('I','g').replace('E','G').replace('B','G').replace('C','G').replace('*','')

    clean_hyp_fh = open(os.path.join(out_dir, "clean_hyp"), "w")
    clean_ref_fh = open(os.path.join(out_dir, "clean_ref"), "w")

    for key, value in hyp_data.items():
        clean_hyp_fh.write(key + " " + value + os.linesep)
    clean_hyp_fh.close()

    for key, value in ref_data.items():
        clean_ref_fh.write(key + " " + value + os.linesep)
    clean_ref_fh.close()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--ref-file', help='path to reference file')
    parser.add_argument('--hyp-file', help='hyp to reference file')
    parser.add_argument('--out-dir', help='path to output directory where clean files will be written.')
    args = parser.parse_args()
    match_files(args.ref_file, args.hyp_file, args.out_dir)
    print("FBank features extracted successfully...")