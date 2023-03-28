from newspaper import Article, Config
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
from pegasus_model import PegasusModel

if __name__ == "__main__":
    model = PegasusModel(save_model_path='model-checkpoint', save_tokenizer_path='tokenizer-checkpoint')
    