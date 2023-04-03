import torch
from torch import nn
from transformers import LukeForQuestionAnswering, AutoTokenizer
from transformers import pipeline


class LukeModel(nn.module):
    def __init__(self, model_name="studio-ousia/luke-base"):
        self.luke = LukeForQuestionAnswering.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
    def forward(self, text, question):
        inputs = self.tokenizer(question, text, return_tensors='pt')
        outputs = self.luke(**inputs)
        
        