from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io

# Load the BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()

# Image preprocessing function
def preprocess_image(image):
    return processor(images=image, return_tensors="pt")

# Caption generation function
def generate_caption(image_tensor):
    with torch.no_grad():
        inputs = preprocess_image(image_tensor)
        outputs = model.generate(
            **inputs,
            max_length=20,
            num_beams=5,
            repetition_penalty=2.0
        )
        caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

# Endpoint to handle image upload and generate caption
@app.route('/generate-caption', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read())).convert("RGB")
    caption = generate_caption(image)
    return jsonify({"caption": caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
