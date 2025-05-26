from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch
import json
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer("all-MiniLM-L6-v2", device=device)

dataset = []
question_embeddings = None

@app.on_event("startup")
def load_dataset():
    global dataset, question_embeddings

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "qa_dataset.json")

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    questions = [item["question"] for item in dataset]
    question_embeddings = model.encode(questions, convert_to_tensor=True, device=device)

@app.post("/predict")
def predict(data: ChatRequest):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    query = data.message.strip()
    query_embedding = model.encode(query, convert_to_tensor=True, device=device)
    cos_scores = util.pytorch_cos_sim(query_embedding, question_embeddings)[0]

    best_score, best_idx = torch.max(cos_scores, dim=0)
    best_score_value = best_score.item()
    best_item = dataset[best_idx]

    # Set your threshold for relevance
    threshold = 0.55

    if best_score_value >= threshold:
        return {
            "response": best_item["answer"],
            "matched_question": best_item["question"],
            "topic": best_item["topic"]
        }
    else:
        return {
            "response": "Sorry, incorrect question."
        }
