import gradio as gr
from app import tokenizer, model
import torch

def predict_log(text):
    # Process input using the model from app.py
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    
    # Return both the prediction and confidence scores
    probabilities = torch.nn.functional.softmax(logits, dim=1)[0].tolist()
    
    # Create a dictionary of class labels and their probabilities
    # Adjust the class names based on your model's actual classes
    class_names = ["Normal", "Anomaly"]  # Replace with your actual class names
    result = {class_names[i]: round(prob * 100, 2) for i, prob in enumerate(probabilities)}
    
    return result, class_names[prediction]

# Create Gradio Interface
demo = gr.Interface(
    fn=predict_log,
    inputs=gr.Textbox(lines=5, placeholder="Enter log text here..."),
    outputs=[
        gr.Label(label="Confidence Scores"),
        gr.Textbox(label="Prediction")
    ],
    title="LLogBERT Log Anomaly Detector",
    description="Enter a log message to classify it as normal or anomalous.",
    examples=[
        ["2023-07-01 12:34:56 INFO Starting application normally"],
        ["2023-07-01 12:34:56 ERROR Failed to connect to database: Connection refused"]
    ]
)

if __name__ == "__main__":
    demo.launch()