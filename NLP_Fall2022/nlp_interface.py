# Hello World

from newspaper import Article
from transformers import AutoConfig, AutoTokenizer, AutoModel
import pandas as pd
from transformers import PegasusForConditionalGeneration, AutoTokenizer
from newspaper import Config
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from summarizer import Summarizer
import torch

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
config = Config()
config.browser_user_agent = user_agent
## prevents timing out ...
config.request_timeout = 30


def summarize_url(url: str) -> str:
    article = Article(url)

    article.download()
    article.parse()

    return summarize_text_pegasus(article.text)


def summarize_text_pegasus(text: str) -> str:
    model_name = "google/pegasus-multi_news"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
    batch = tokenizer(text, truncation=True, padding="longest", return_tensors="pt").to(
        device
    )
    translated = model.generate(**batch)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return tgt_text


if __name__ == "__main__":
    print(
        summarize_url(
            "https://www.npr.org/2022/11/12/1136205315/musk-twitter-bankruptcy-how-likely"
        )
    )
