#!/usr/bin/env bash
set -x
# Always check these paths before starting the preprocessing.
# ws is the workspace containing both the ASR_Datasets dir and the icefall repository.
# repo is the path to the custom_asr directory.
# train_dataset is the direcotry for training. should contain wav.scp, text_lexicon.txt
ws=/home/mselim
asr_datasets=$ws/ASR_Datasets
train_dataset=/home/mselim/without_codeswitches/original_data/MGB3/mgb3_dev_data/Omar   ##### TODO: Change to directory containing Kaldi style metadata.
custom_repo=$ws/icefall_ws/icefall_custom3000/icefall/egs/librispeech/custom_asr        ##### TODO: Change to custom_asr under the specific repo path
exp_dir=$ws/icefall_ctc_exp_3000/                                                       ##### TODO: Change to experiments directory
dataset_name=mgb3Omar                                                                   ##### TODO: Change to dataset nameVery Imporant
dataset_type=val # It should be train, test or val                                      ##### TODO: Change to dataset type

cd $custom_repo

chmod u+x scripts/*
chmod u+x stage*.sh

mkdir -p data/colloquial_arabic/
mkdir -p download/colloquial_lm/
mkdir -p $exp_dir

cp $train_dataset/wav.scp $train_dataset/wav.scp_safe 

python scripts/create_segments.py --scp-file $train_dataset/wav.scp --output-file $train_dataset/segments 

python scripts/clean_data.py --input-scp $train_dataset/wav.scp_safe --input-seg $train_dataset/segments --input-text $train_dataset/text --output-dir $train_dataset/

#python scripts/merge_lexicons.py --lex1-file $asr_datasets/KenLM/language_model_training_data_lexicon.txt --lex2-file $train_dataset/text_lexicon.txt --output-file $asr_datasets/KenLM/lexicon.txt

python scripts/create_manifests.py --kaldi-dir $train_dataset --dataset-name $dataset_name --dataset-type $dataset_type --output-dir $custom_repo/data/colloquial_arabic/ 

./scripts/compute_fbank_asr.py --dataset-name $dataset_name

cp -r $asr_datasets/KenLM/* download/colloquial_lm/

./stage5.sh
./stage6.sh 
./stage7.sh
./stage8.sh
./stage9.sh
./stage10.sh
