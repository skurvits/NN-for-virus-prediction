#!/bin/bash
#SBATCH -J gen-net-job
#SBATCH --time=1:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=yourmail@gmail.com
#SBATCH --partition=gpu
#SBATCH --gres=gpu:tesla:1
#SBATCH --mem=32000
#SBATCH --cpus-per-task=4

module load python/3.6.3/CUDA-9.0

# This is a runner script for running some python scripts in SLURM
# Use for bigger jobs.
#
# Run it like that:
# runGPU.sh script.py --par1 value1 --par2 value2 ...
# ... or just paste the command below
#
# TODO: Activate the virus-nn enviroment first!
# TODO: EMAIL and TIME fields!

# CUDA for GPUs - 0 = 1 gpu; 1 = 2 gpus...
export CUDA_VISIBLE_DEVICES=0
# add some deps https://github.com/tensorflow/tensorflow/issues/20271
export LD_LIBRARY_PATH=/storage/software/python/3.6.3/CUDA-9.0/pkgs/cudnn-7.1.2-cuda9.0_0/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/storage/software/python/3.6.3/CUDA-9.0/pkgs/cudatoolkit-9.0-h13b8566_0/lib/:$LD_LIBRARY_PATH

# Start your script
# python "$@"

# or just run it here:
python frequency_branch.py ./out/freq_test \
	--input_path ./data/DNA_data/fullset  \
	--epochs 3 \
	--filter_size 8 \
	--layer_sizes 1000 \
	--dropout 0.1 \
	--learning_rate 0.001 \
	--lr_decay None

