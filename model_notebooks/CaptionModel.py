import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load the BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()  # Set the model to evaluation mode

# Function to generate captions for an image
def generate_caption(image_path):
    # Open the image in RGB mode
    image = Image.open(image_path).convert("RGB")
    
    # Process the image and prepare inputs for the model
    inputs = processor(images=image, return_tensors="pt")
    
    # Generate the caption without training or fine-tuning
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=20,          # Set maximum length for the caption
            num_beams=5,            # Use beam search for better quality
            repetition_penalty=2.0  # Penalize repetitive text
        )
        
    # Decode the generated caption
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    return caption

# Example usage
image_path = "/home/nancy/Media-Insight/backend/static/descriptions_images/panda.png"  # Replace with your image path
caption = generate_caption(image_path)
print("Generated caption:", caption)
