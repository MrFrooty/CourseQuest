import json
import os
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
from datasets import load_dataset, Dataset, load_metric

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("deepset/xlm-roberta-large-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/xlm-roberta-large-squad2")

# Load your dataset
dataset = load_dataset("json", data_files={"train": "catalog.json"})

# Preprocess the dataset
def preprocess_function(examples):
    contexts = []
    questions = []
    answers = []
    start_positions = []

    for example in examples['paragraphs']:
        context = example['context']
        for qa in example['qas']:
            contexts.append(context)
            questions.append(qa['question'])
            answers.append(qa['answers'][0]['text'])
            start_positions.append(qa['answers'][0]['answer_start'])

    tokenized_examples = tokenizer(
        questions, contexts, truncation=True, padding="max_length", max_length=384
    )

    tokenized_examples["start_positions"] = start_positions
    tokenized_examples["end_positions"] = [
        start + len(answer) for start, answer in zip(start_positions, answers)
    ]

    return tokenized_examples

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["train"],
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")