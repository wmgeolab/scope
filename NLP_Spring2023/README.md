# SCOPE NLP Spring 2023

This directory contains all the necessary files for using the Pegasus language model for summaries as well as using torchserve to host the model for inference through a REST api.

## Setup Information

First you need to setup an anaconda environment from the `conda_environment.yml` file that has all the dependencies necessary to run everything. *DISCLAIMER*: `pegasus_model.py` and `nlp_inferface.py` work perfectly fine on windows, but torchserve will not function properly unless loaded on a linux machine. The easiest way to do this is by starting up a Ubuntu 18.04 VM through WSL 2 and installing openjdk17.

### Linux Environment Setup

Once you have an Ubuntu 18.04 VM running on WSL 2 or some other source, setting up the environment is fairly easy:

1. Install openjdk17: `sudo apt-get install openjdk-17-jdk`
2. Load conda environment using: `conda env create -f environment.yml`
3. Activate conda environment: `conda activate scope_nlp`
4. Done

### Creating Model Archive (MAR) File

Before the model can be hosted for inference with TorchServe, it must be archived into the `.MAR` format. This is done by using the `torch-model-archiver` package which should already be installed from setting up the linux environment.

1. First execute the `create_checkpoints.py` file to save the pegasus model files as well as the tokenizer files.
2. Now you can run `torch-model-archiver` to create the archive with the following command.

``` Shell
torch-model-archiver --model-name PegasusSummarizer3 --model-file pegasus_model.py --handler PegasusHandler.py --serialized-file model-checkpoint/pytorch_model.bin --extra-files tokenizer-checkpoint/spiece.model,tokenizer-checkpoint/tokenizer_config.json,tokenizer-checkpoint/special_tokens_map.json,model-checkpoint/config.json --export-path torchserve/model_store --version 3.0
```

3. Now check to make sure there is a file called `PegasusSummarizer3.mar` in `torchserve/model_store`.