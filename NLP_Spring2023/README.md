# SCOPE NLP Spring 2023

This directory contains all the necessary files for using the Pegasus language model for summaries as well as using torchserve to host the model for inference through a REST api.

---

## Setup Information

First you need to setup an anaconda environment from the `conda_environment.yml` file that has all the dependencies necessary to run everything. *DISCLAIMER*: `pegasus_model.py` and `nlp_inferface.py` work perfectly fine on windows, but torchserve will not function properly unless loaded on a linux machine. The easiest way to do this is by starting up a Ubuntu 18.04 VM through WSL 2 and installing openjdk17.

