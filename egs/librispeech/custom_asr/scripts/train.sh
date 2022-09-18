#!/usr/bin/env bash
set -x
# Always check these paths before starting the preprocessing.
# ws is the workspace containing both the ASR_Datasets dir and the icefall repository.
# repo is the path to the custom_asr directory.
# train_dataset is the direcotry for training. should contain wav.scp, text_lexicon.txt
ws=/home/mselim
asr_datasets=$ws/ASR_Datasets
train_dataset=$asr_datasets/original_data/Train_Data/train_data
custom_repo=$ws/icefall_ws/icefall_custom/icefall/egs/librispeech/custom_asr
exp_dir=$ws/icefall_ctc_exp_1000/

cd $custom_repo
python conformer_ctc/custom_train.py --start-epoch 55 --num-epochs 63 --max-duration 50 --world-size=4 --lang-dir=data/lang_bpe_5000 --exp-dir=$exp_dir
