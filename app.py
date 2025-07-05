from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizerFast, BertForSequenceClassification, BertConfig
import torch

app = FastAPI()

# Define the input model expected in POST /predict
class InputText(BaseModel):
    text: str

# Step 1: Load the custom tokenizer
try:
    tokenizer = BertTokenizerFast.from_pretrained(
        ".",  # assumes tokenizer.json, vocab.txt, etc. are in the same directory
        tokenizer_file="tokenizer.json"
    )
except Exception as e:
    raise RuntimeError(f"Failed to load tokenizer: {e}")

# Step 2: Load model configuration
try:
    config = BertConfig.from_json_file("config.json")
except Exception as e:
    raise RuntimeError(f"Failed to load model config: {e}")

# Step 3: Initialize model and load state_dict
try:
    model = BertForSequenceClassification(config)
    #state_dict = torch.load("vhm_center.pt", map_location=torch.device("cpu"))
    state_dict = torch.load("vhm_center.pt", map_location="cpu")
    print(f"state_dict.keys ======= {state_dict.keys} \n\n\n")

    #model.load_state_dict(state_dict)
    load_result = model.load_state_dict(state_dict, strict=False)

    print("❌ Missing keys:", load_result.missing_keys)
    print("❗ Unexpected keys:", load_result.unexpected_keys)

    model.eval()
except Exception as e:
    raise RuntimeError(f"Failed to load model from vhm_center.pt: {e}")

# Step 4: Define the input format
class InputText(BaseModel):
    text: str

# Health check
@app.get("/")
def read_root():
    return {"message": "LLogBERT API is running!"}

# Prediction endpoint
@app.post("/predict")
def predict(req: InputText):
    try:
        inputs = tokenizer(req.text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=1).item()
        return {"label": prediction, "logits": logits.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
