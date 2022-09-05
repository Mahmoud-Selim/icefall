import sys
import shutil
import argparse
import os

def main(lex1_file, lex2_file, output_file):
    lex1_fh = open(lex1_file)
    lex2_fh = open(lex2_file)
    out_fh = open(output_file,"w")


    existing_files = set()
    
    for line in lex1_fh:
        word = line.split()[0]

        if(word in existing_files):
            continue 
        
        existing_files.add(word)

        out_fh.write(line)
        #out_fh.write("\n")

    for line in lex2_fh:
        word = line.split()[0]

        if(word in existing_files):
            continue 
        
        existing_files.add(word)

        out_fh.write(line)
        #out_fh.write("\n")


    out_fh.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--lex1-file', help='path to first lexicon file')
    parser.add_argument('--lex2-file', help='path to second lexicon file')
    parser.add_argument('--output-file', help='Directory of new path')
    args = parser.parse_args()
    main(args.lex1_file, args.lex2_file, args.output_file)
