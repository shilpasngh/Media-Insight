import os
import logging
from abc import ABC, abstractmethod
from config import Config
from dotenv import load_dotenv
import pymongo
import torch
from diffusers import AmusedPipeline
from bson import ObjectId
from preload_models import blip_model, processor  # Import preloaded BLIP model and processor
from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, '.env')
load_dotenv(path)
upload_path = os.path.join(basedir, 'static/descriptions_images/')

client = pymongo.MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DB]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskModel(ABC):
    def __init__(self, message_data):
        self.message_data = message_data
    
    @abstractmethod
    def run(self):
        pass

# Use Case 1: Generate an image from a text prompt
class Text2ImageModel(TaskModel):
    def run(self):
        self.text2image_task(self.message_data)

    def update_task(self, _id, image_path):
        collection = db['text2image']
        result = collection.find_one({'_id': ObjectId(_id)})
        # write the name of the image to the database
        collection.update_one({'_id': ObjectId(_id)}, {'$set': {'image': image_path}})
        return result

    def text2image_task(self, data):
        # Load the model in fp32 precision (default for CPU)
        pipe = AmusedPipeline.from_pretrained(
            "amused/amused-256", torch_dtype=torch.float32
        )

        # Move the model to CPU
        pipe = pipe.to("cpu")

        # Define the prompt and negative prompt
        prompt = data['text']
        negative_prompt = ""

        # Generate the image on CPU
        image = pipe(prompt, negative_prompt=negative_prompt, generator=torch.manual_seed(0)).images[0]

        # Display or return the image
        image_path = f"{data['task_id']}.png"
        image.save(f"{basedir}/static/images/" + image_path)

        self.update_task(data['task_id'], image_path)

# Use Case 2: Generate a description from an image
class GenerateDescriptionModel(TaskModel):
    def run(self):
        self.generate_description_task(self.message_data)

    def generate_description_task(self, data):
        # Save the uploaded image
        image_path = f"{data['task_id']}"
        image_full_path = os.path.join(basedir, "static/descriptions_images", image_path)

        # Generate the caption
        caption = self.generate_caption(image_full_path)

        # Save the generated caption and image path in MongoDB
        self.update_task(data['task_id'], caption)

    def update_task(self, _id, caption):
        collection = db['generate-description']
        collection.update_one(
            {'_id': ObjectId(_id)},
            {'$set': {'caption': caption}}
        )

    def generate_caption(self, image_path):
        # Open the image, process it, and generate a caption
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        
        with torch.no_grad():
            outputs = blip_model.generate(
                **inputs,
                max_length=20,
                num_beams=5,
                repetition_penalty=2.0
            )
        
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption

# Use Case 3: Summarize a text
class GenerateTextModel(TaskModel):
    def run(self):
        pass
