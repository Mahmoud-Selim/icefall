#!/bin/sh
#SBATCH --nodes=1
#SBATCH --job-name=ASR_K2_training
#SBATCH --time=23:59:00
#SBATCH --output=/home/mselim/icefall_ctc_exp_1000/asr_k2_1000%j%x.out
#SBATCH --error=/home/mselim/icefall_ctc_exp_1000/asr_k2_1000%j%x.err
#SBATCH --partition=gpu
#SBATCH --ntasks=1
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task=1
#SBATCH --exclusive

module load singularity/3.7.1
export SINGULARITY_CACHEDIR=/home/mselim/sing_cache/
export SINGULARITY_TMPDIR=/home/mselim/sing_tmp/
cd /home/mselim/icefall_ws/icefall_custom/icefall/egs/librispeech/custom_asr/
singularity run --nv --writable /home/mselim/sing_sifs/icefall_nv.img/ ./scripts/train.sh


