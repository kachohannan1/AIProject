import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle

# Load marketing Q&A JSON file
with open("qa_dataset.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(qa_data)

# Create prompts and labels
df['prompt'] = df['question']
df['label_text'] = df['answer']

label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label_text'])

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

class QADataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding="max_length", max_length=64, return_tensors="pt")
        self.labels = torch.tensor(labels)

    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

X_train, X_val, y_train, y_val = train_test_split(df['prompt'], df['label'], test_size=0.2, random_state=42)

train_dataset = QADataset(X_train.tolist(), y_train.tolist())
val_dataset = QADataset(X_val.tolist(), y_val.tolist())


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(label_encoder.classes_))
model.to(device)

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=3,
    logging_dir="./logs",
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Train the model
trainer.train()

model.save_pretrained("./bert_marketing_model")
tokenizer.save_pretrained("./bert_marketing_model")

print(" Training complete and model saved.")
