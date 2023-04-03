import torch
from torch import nn
from transformers import LukeForQuestionAnswering, AutoTokenizer
from transformers import pipeline


class LukeModel(nn.Module):
    def __init__(self, model_name="studio-ousia/luke-base"):
        #self.luke = LukeForQuestionAnswering.from_pretrained(model_name)
        #self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.LukeQA = pipeline(model=model_name, tokenizer=model_name, task='text2text-generation', framework='pt')
        
    def forward(self, text, question):
        # inputs = self.tokenizer(question, text, return_tensors='pt')
        # outputs = self.luke(**inputs)
        pass
    
    def test_pipeline(self):
        return self.LukeQA("question: Where do I live? context: My name is Wolfgang and I live in Berlin")

if __name__ == "__main__":
    model = LukeModel()
    
    print(f"Output: {model.test_pipeline()}")
