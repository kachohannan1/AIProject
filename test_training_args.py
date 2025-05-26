from transformers import TrainingArguments

print("TrainingArguments imported")

args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=1,
)

print("TrainingArguments initialized successfully")
