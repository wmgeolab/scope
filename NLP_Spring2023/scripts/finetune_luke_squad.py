"""LUKE Fine-tuning Script

This script is for fine-tuning the LUKE transformer model to answer questions with the Stanford SQUAD dataset.
"""
from functools import partial

from transformers import LukeForQuestionAnswering, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
from wandb import login, init
from torch.nn import CrossEntropyLoss
from transformers.data.processors.squad import SquadV1Processor
from transformers import squad_convert_examples_to_features


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
        report_to=["wandb"],
    )


# Tokenize the input data
def tokenize_function(examples, tokenizer):
    return tokenizer(
        examples["question"],
        examples["context"],
        truncation="only_second",
        max_length=512,
        padding="max_length",
    )


def compute_loss(model, inputs):
    start_positions = inputs.pop("start_positions")
    end_positions = inputs.pop("end_positions")
    outputs = model(**inputs)
    start_logits, end_logits = outputs.start_logits, outputs.end_logits
    ce_loss_fct = CrossEntropyLoss()
    start_loss = ce_loss_fct(start_logits, start_positions)
    end_loss = ce_loss_fct(end_logits, end_positions)
    total_loss = (start_loss + end_loss) / 2
    return total_loss


if __name__ == "__main__":
    LukeTokenizer = AutoTokenizer.from_pretrained("studio-ousia/luke-base")

    processor = SquadV1Processor()

    squad = load_dataset("squad")

    squad.set_format("torch")

    train_features = processor.get_examples_from_dataset(squad)

    print(f"Train Features: {train_features}")

    tokenize = partial(tokenize_function, tokenizer=LukeTokenizer)

    # train_dataset = train_dataset.map(tokenize, batched=True)
    # eval_dataset = eval_dataset.map(tokenize, batched=True)
    #
    # print(f"Squad: {train_dataset}")
    # print(f"Answers: {train_dataset['answers'][0]}")
    # print(f"Context: {train_dataset['context'][0]}")
    # print(f"Question: {train_dataset['question'][0]}")

    # # Weights and Biases Integration
    # login()
    # init(
    #     project="Luke-Question-Answering",
    #     name="TestRun0",
    # )
    #
    # training_args = get_training_arguments()
    # trainer = Trainer(
    #     model=LukeModel,
    #     args=training_args,
    #     compute_loss=compute_loss,
    #     eval_dataset=eval_dataset,
    #     train_dataset=train_dataset,
    # )
    #
    # trainer.train()





    # training_args = get_training_arguments(output_dir="Test1")
    # trainer_object = create_trainer(
    #     model=LukeForQuestionAnswering.from_pretrained("studio-ousia/luke-base"),
    #     args=training_args,
    #     train_dataset=squad["train"],
    #     eval_dataset=squad["validation"],
    #     data_collator=DefaultDataCollator(),
    #     tokenizer=LukeTokenizer
    # )
    #
    # trainer_object.train()
