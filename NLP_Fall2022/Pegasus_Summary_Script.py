from newspaper import Article
from transformers import AutoConfig, AutoTokenizer, AutoModel
from summarizer import Summarizer
import pandas as pd
from transformers import PegasusForConditionalGeneration, AutoTokenizer
import torch
from newspaper import Config
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch



# Change this to be whatever URL(s) you want to summarize.
# We can discuss I/O format in the future.
# Purpose of this code is to provide a base script.
urls = ["https://ai.googleblog.com/2020/06/pegasus-state-of-art-model-for.html"]
for item in urls:

    ## fixes browser block ...
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    ## prevents timing out ...
    config.request_timeout = 30
    try:
        ## Get article text.
        article = Article(url, config=config)
        article.download()
        article.parse()
        txt = article.text
        # Multi_news has performed well so far.
        model_name = 'google/pegasus-multi_news'
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
        batch = tokenizer(txt, truncation=True, padding='longest', return_tensors="pt").to(device)
        translated = model.generate(**batch)
        tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
        results[url] = tgt_text
    except Exception as e:
        print(e)
