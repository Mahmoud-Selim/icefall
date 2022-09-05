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

log "Stage 8: Prepare G"
# We assume you have install kaldilm, if not, please install
# it using: pip install kaldilm

mkdir -p data/lm
if [ ! -f data/lm/G_3_gram.fst.txt ]; then
# It is used in building HLG
python3 -m kaldilm \
    --read-symbol-table="data/lang_phone/words.txt" \
    --disambig-symbol='#0' \
    --max-order=3 \
    $dl_dir/colloquial_lm/3gram.arpa > data/lm/G_3_gram.fst.txt
fi

if [ ! -f data/lm/G_4_gram.fst.txt ]; then
# It is used for LM rescoring
python3 -m kaldilm \
    --read-symbol-table="data/lang_phone/words.txt" \
    --disambig-symbol='#0' \
    --max-order=4 \
    $dl_dir/colloquial_lm/4gram.arpa > data/lm/G_4_gram.fst.txt
fi
