import torch
from transformers import LukeForQuestionAnswering, AutoTokenizer, Trainer, TrainingArguments
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
        max_grad_norm=None,
        lr_scheduler_type='linear',
        warmup_ratio=0.06,   
    )
    
def get_train_eval_datasets(train_eval_split=0.2):
    squad = load_dataset("squad", split="train[:5000]")
    squad = squad.train_test_split(test_size=train_eval_split)
    
    print(f"First example in dataset: \n {squad['train'][0]}")
    
if __name__ == "__main__":
    args = get_training_arguments()
    
    get_train_eval_datasets()
    