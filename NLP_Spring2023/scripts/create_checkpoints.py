"""Pegasus Checkpoint Generator

This script loads the pegasus model from its definition file and saves
the pretrained weights to 'model-checkpoint' for the transformer and
'tokenizer-checkpoint' for the tokenizer which contain all necessary
files for using the pegasus model.
"""

from pegasus_model import PegasusModel


def generate_checkpoints():
    _ = PegasusModel(
        save_model_path="model-checkpoint", save_tokenizer_path="tokenizer-checkpoint"
    )


if __name__ == "__main__":
    generate_checkpoints()
