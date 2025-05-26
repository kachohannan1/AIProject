import pickle

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

print(label_encoder.classes_)
