# Hello World

from newspaper import Article, Config
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import os

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
config = Config()
config.browser_user_agent = user_agent
## prevents timing out ...
config.request_timeout = 30

TORCH_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Torch Device: {TORCH_DEVICE}")


class SummaryFactory:
    """Class to deal with initializing the PEGASUS model and querying it with urls"""

    def __init__(self):
        self.model_initialized = False
        self.model, self.tokenizer = self.initialize_pegasus_model()

    def initialize_pegasus_model(self):
        """Initializes the pegasus model and its tokenizer with the pretrained weights from hugging face"""

        model_name = "google/pegasus-multi_news"

        model = PegasusForConditionalGeneration.from_pretrained(model_name).to(
            TORCH_DEVICE
        )
        tokenizer = PegasusTokenizer.from_pretrained(model_name)

        self.model_initialized = True

        return model, tokenizer

    def summarize_url(self, url: str) -> str:
        article = Article(url)
        article.download()
        article.parse()

        return self.summarize_text_pegasus(article.text)

    def summarize_text_pegasus(self, text: str) -> str:
        batch = self.tokenizer(
            text, truncation=True, padding="longest", return_tensor="pt"
        ).to(TORCH_DEVICE)
        translated = self.model.generate(**batch)
        tgt_text = self.tokenizer.batch_decode(translated, skip_special_tokens=True)

        return tgt_text


if __name__ == "__main__":
    factory = SummaryFactory()

    factory.initialize_pegasus_model()

    factory.summarize_url(
        "https://www.npr.org/2022/11/12/1136205315/musk-twitter-bankruptcy-how-likely"
    )
