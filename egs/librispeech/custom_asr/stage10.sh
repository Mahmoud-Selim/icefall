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

log "Stage 10: Compile LG"
./local/compile_lg.py --lang-dir data/lang_phone

for vocab_size in ${vocab_sizes[@]}; do
lang_dir=data/lang_bpe_${vocab_size}
./local/compile_lg.py --lang-dir $lang_dir
done
