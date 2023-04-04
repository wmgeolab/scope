import torch
from torch import nn
from transformers import LukeForQuestionAnswering, AutoTokenizer
from transformers import pipeline


class LukeModel(nn.Module):
    def __init__(self, model_name="studio-ousia/luke-base", *args, **kwargs):
        super(LukeModel, self).__init__(*args, **kwargs)
        self.luke = LukeForQuestionAnswering.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # self.LukeQA = pipeline(
        #     model=model_name,
        #     tokenizer=model_name,
        #     task="text2text-generation",
        #     framework="pt",
        # )

    def forward(self, text, question):
        inputs = self.tokenizer(question, text, return_tensors="pt")
        outputs = self.luke(**inputs)

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()

        predict_answer_tokens = inputs.input_ids[
            0, answer_start_index : answer_end_index + 1
        ]

        print(f"Outputs Ids: {outputs}")
        print(f"Predict_answer_tokens: {predict_answer_tokens}")
        print(
            f"Decoded prediction: {self.tokenizer.decode(predict_answer_tokens, skip_special_tokens=True)}"
        )

    def test_pipeline(self):
        return self.LukeQA(
            "question: Where do I live? context: My name is Wolfgang and I live in Berlin"
        )


if __name__ == "__main__":
    model = LukeModel()

    question, text = (
        "Who was Jim Henson?",
        "Jim Henson was a nice puppet that liked to go on runs in the evening",
    )

    print(f"Output: {model.forward(text, question)}")
