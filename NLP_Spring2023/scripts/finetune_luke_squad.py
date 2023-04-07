"""LUKE Fine-tuning Script

This script is for fine-tuning the LUKE transformer model to answer questions with the Stanford SQUAD dataset.
"""
from functools import partial

from transformers import (
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    AutoModelForQuestionAnswering,
    DefaultDataCollator,
)
from datasets import load_dataset
from wandb import login, init


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
        lr_scheduler_type="linear",
        warmup_ratio=0.06,
        report_to=["wandb"],
    )


def preprocess_function(examples, tokenizer):
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


def initialize_wandb():
    login()
    init(
        project="Luke-Question-Answering",
        name="TestRun0",
    )


if __name__ == "__main__":
    model_name = "xlnet-base-cased"

    # Load Squad Dataset
    squad = load_dataset("squad")

    # Get tokenizer and preprocess data
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    preprocessor = partial(preprocess_function, tokenizer=tokenizer)
    tokenized_squad = squad.map(
        preprocessor, batched=True, remove_columns=squad["train"].column_names
    )

    # Load Model
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    training_args = get_training_arguments()

    trainer_object = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_squad["train"],
        eval_dataset=tokenized_squad["validation"],  # Might not be called test
        tokenizer=tokenizer,
        data_collator=DefaultDataCollator(),
    )

    trainer_object.train()
