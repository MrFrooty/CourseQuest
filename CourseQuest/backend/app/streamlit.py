import json
import os
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, TrainingArguments, Trainer
from datasets import load_dataset, DatasetDict

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

    for data_item in examples["data"]:
        for paragraph in data_item["paragraphs"]:
            context = paragraph["context"]
            for qa in paragraph["qas"]:
                contexts.append(context)
                questions.append(qa["question"])
                answers.append(qa["answers"][0]["text"])
                start_positions.append(qa["answers"][0]["answer_start"])

    tokenized_examples = tokenizer(
        questions, contexts, truncation=True, padding="max_length", max_length=384
    )

    tokenized_examples["start_positions"] = start_positions
    tokenized_examples["end_positions"] = [
        start + len(answer) for start, answer in zip(start_positions, answers)
    ]

    return tokenized_examples

# Custom function to handle the nested structure
def custom_map_function(batch):
    processed_batch = {
        "input_ids": [],
        "attention_mask": [],
        "start_positions": [],
        "end_positions": []
    }
    for data_item in batch["data"]:
        tokenized_example = preprocess_function([data_item])
        processed_batch["input_ids"].extend(tokenized_example["input_ids"])
        processed_batch["attention_mask"].extend(tokenized_example["attention_mask"])
        processed_batch["start_positions"].extend(tokenized_example["start_positions"])
        processed_batch["end_positions"].extend(tokenized_example["end_positions"])
    return processed_batch

# Apply the custom mapping function
tokenized_dataset = dataset["train"].map(custom_map_function, batched=True)

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
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
