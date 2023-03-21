# Hello World

from newspaper import Article, Config
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
from pegasus_model import PegasusModel


class SummaryFactory:
    """Class to deal with initializing the PEGASUS model and querying it with urls"""

    def __init__(self):
        self.model = PegasusModel()
        print(f"Model being loaded on device: {self.model.TORCH_DEVICE}")

        self.initialize_newspaper_config()

    def initialize_newspaper_config(self):
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        config = Config()
        config.browser_user_agent = user_agent
        ## prevents timing out ...
        config.request_timeout = 30

    def summarize_url(self, url: str) -> str:
        article = Article(url)
        article.download()
        article.parse()

        return self.model(article.text)


if __name__ == "__main__":
    factory = SummaryFactory()

    print(
        factory.summarize_url(
            "https://www.npr.org/2022/11/12/1136205315/musk-twitter-bankruptcy-how-likely"
        )
    )
