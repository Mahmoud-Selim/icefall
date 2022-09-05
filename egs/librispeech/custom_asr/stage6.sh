#!/usr/bin/env bash

set -eou pipefail
dl_dir=$PWD/download

vocab_sizes=(
  5000
  2000
  1000
  500
)

log() {
  # This function is from espnet
  local fname=${BASH_SOURCE[1]##*/}
  echo -e "$(date '+%Y-%m-%d %H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}

log "Stage 6: Prepare BPE based lang"

for vocab_size in ${vocab_sizes[@]}; do
lang_dir=data/lang_bpe_${vocab_size}
mkdir -p $lang_dir
# We reuse words.txt from phone based lexicon
# so that the two can share G.pt later.
cp data/lang_phone/words.txt $lang_dir

if [ ! -f $lang_dir/transcript_words.txt ]; then
    log "Generate data for BPE training"
    files=$(
    find "/home/mselim/ASR_Datasets/Train_Data/sub_train_data_100h/text"
    )
    for f in ${files[@]}; do
    cat $f | cut -d " " -f 2-
    done > $lang_dir/transcript_words.txt
fi

if [ ! -f $lang_dir/bpe.model ]; then
    ./local/train_bpe_model.py \
    --lang-dir $lang_dir \
    --vocab-size $vocab_size \
    --transcript $lang_dir/transcript_words.txt
fi

if [ ! -f $lang_dir/L_disambig.pt ]; then
    ./local/prepare_lang_bpe.py --lang-dir $lang_dir

    log "Validating $lang_dir/lexicon.txt"
    ./local/validate_bpe_lexicon.py \
    --lexicon $lang_dir/lexicon.txt \
    --bpe-model $lang_dir/bpe.model
fi
done
