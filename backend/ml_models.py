import os
import logging
from abc import ABC, abstractmethod
from config import Config
from dotenv import load_dotenv
import pymongo
import torch
from diffusers import AmusedPipeline
from bson import ObjectId

basedir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(basedir, '.env')
load_dotenv(path)

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
        # prompt = "A mecha robot in a favela in expressionist style, with a sunset in the background"
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
        pass

# Use Case 3: Summarize a text
class GenerateTextModel(TaskModel):
    def run(self):
        pass
