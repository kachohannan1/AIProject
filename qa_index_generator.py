# qa_index_generator.py
import json
import pickle
from sentence_transformers import SentenceTransformer

# Load the new dataset
with open("qa_dataset.json", "r", encoding="utf-8") as f:
    qa_data = json.load(f)

questions = [item["question"] for item in qa_data]
answers = [item["answer"] for item in qa_data]
topics = [item["topic"] for item in qa_data]  # Optional, for enhanced retrieval

# Encode questions using SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(questions, convert_to_tensor=False)

# Save the index
with open("qa_index.pkl", "wb") as f:
    pickle.dump({
        "questions": questions,
        "answers": answers,
        "topics": topics,  # include this
        "embeddings": [e.tolist() for e in embeddings],
    }, f)

print("✅ QA index saved.")
