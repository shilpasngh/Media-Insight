from diffusers import AmusedPipeline
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

pipe = AmusedPipeline.from_pretrained(
            "amused/amused-256", torch_dtype=torch.float32
        )

# Load the BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
# blip_model.eval()  # Set the model to evaluation mode
