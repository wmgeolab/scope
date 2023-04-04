"""LUKE Fine-tuning Script

This script is for fine-tuning the LUKE transformer model to answer questions with the Stanford SQUAD dataset.
"""


import torch
from transformers import LukeConfig, LukeForQuestionAnswering, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset


def create_trainer(model, args: TrainingArguments, train_dataset, eval_dataset, tokenizer, data_collator):
    """Creates a Trainer object based on training arguments, datasets, tokenizer and data collator."""
    
    return Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator
    )
    
    
def get_luke_model_config():
    pass


def get_training_arguments(output_dir=None):
    """Returns the training arguments for finetuning LUKE as specified in the paper."""
    
    return TrainingArguments(
        output_dir="qa_model_default" if not output_dir else output_dir,
        evaluation_strategy="epoch",
        learning_rate=1e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        adam_beta1=0.9,
        adam_beta2=0.98,
        adam_epsilon=1e-6,
        max_grad_norm=1e100,
        lr_scheduler_type='linear',
        warmup_ratio=0.06,
    )


def get_train_eval_datasets(train_eval_split=0.2):
    squad = load_dataset("squad", split="train")
    # squad = squad.train_test_split(test_size=train_eval_split)
    
    print(f"Squad Object: {squad}")
    
    # print(f"First example in dataset: \n {squad['train'][0]}")


def preprocess_function(examples, tokenizer):
    """Preprocess Function from Huggingface Question Answering Guide

    Specifically made to be used with SQUAD
    """

    questions = [q.strip() for q in examples["question"]]
    inputs = tokenizer(
        questions,
        examples["context"],
        max_length=384,
        truncation="only_second",
        return_offsets_mapping=True,
        padding="max_length",
    )

    offset_mapping = inputs.pop("offset_mapping")
    answers = examples["answers"]
    start_positions = []
    end_positions = []

    for i, offset in enumerate(offset_mapping):
        answer = answers[i]
        start_char = answer["answer_start"][0]
        end_char = answer["answer_start"][0] + len(answer["text"][0])
        sequence_ids = inputs.sequence_ids(i)

        # Find the start and end of the context
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # If the answer is not fully inside the context, label it (0, 0)
        if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            # Otherwise it's the start and end token positions
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char:
                idx += 1
            start_positions.append(idx - 1)

            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char:
                idx -= 1
            end_positions.append(idx + 1)

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions

    return inputs


def train_model():
    pass


if __name__ == "__main__":
    arguments = get_training_arguments()
    
    get_train_eval_datasets()
    