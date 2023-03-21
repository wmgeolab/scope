import torch
from torch import nn
from transformers import PegasusForConditionalGeneration, PegasusTokenizer


class PegasusModel(nn.Module):
    def __init__(self, save_path=None):
        super(PegasusModel, self).__init__()

        self.TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        self.TORCH_DEVICE = "cpu"

        self.tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-multi_news")
        self.pegasus = PegasusForConditionalGeneration.from_pretrained(
            "google/pegasus-multi_news"
        ).to(self.TORCH_DEVICE)

    def forward(self, x: str):
        """Do forward pass of model"""

        batch = self.tokenizer(
            x,
            truncation=True,
            padding="longest",
            return_tensors="pt",
        ).to(self.TORCH_DEVICE)

        translated = self.pegasus.generate(**batch)
        tgt_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)

        return tgt_text
