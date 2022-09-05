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

log "Stage 7: Prepare bigram P"

for vocab_size in ${vocab_sizes[@]}; do
lang_dir=data/lang_bpe_${vocab_size}

if [ ! -f $lang_dir/transcript_tokens.txt ]; then
    ./local/convert_transcript_words_to_tokens.py \
    --lexicon $lang_dir/lexicon.txt \
    --transcript $lang_dir/transcript_words.txt \
    --oov "<UNK>" \
    > $lang_dir/transcript_tokens.txt
fi

if [ ! -f $lang_dir/P.arpa ]; then
    ./shared/make_kn_lm.py \
    -ngram-order 2 \
    -text $lang_dir/transcript_tokens.txt \
    -lm $lang_dir/P.arpa
fi

if [ ! -f $lang_dir/P.fst.txt ]; then
    python3 -m kaldilm \
    --read-symbol-table="$lang_dir/tokens.txt" \
    --disambig-symbol='#0' \
    --max-order=2 \
    $lang_dir/P.arpa > $lang_dir/P.fst.txt
fi
done

