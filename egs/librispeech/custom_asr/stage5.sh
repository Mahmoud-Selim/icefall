#!/usr/bin/env bash

set -eou pipefail
dl_dir=$PWD/download

log() {
  # This function is from espnet
  local fname=${BASH_SOURCE[1]##*/}
  echo -e "$(date '+%Y-%m-%d %H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}

log "Stage 5: Prepare phone based lang"

lang_dir=data/lang_phone
mkdir -p $lang_dir

(echo '!SIL SIL'; echo '<SPOKEN_NOISE> SPN'; echo '<UNK> SPN'; ) |
cat - $dl_dir/colloquial_lm/lexicon.txt |
sort | uniq > $lang_dir/lexicon.txt

if [ ! -f $lang_dir/L_disambig.pt ]; then
./local/prepare_lang.py --lang-dir $lang_dir
fi
