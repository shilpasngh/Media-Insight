from confluent_kafka import Consumer, KafkaError
 # Updated import path
import json
import logging
import torch
from diffusers import AmusedPipeline
from bson import ObjectId


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def kafka_consumer(db):
    # Configure the consumer
    consumer_config = {
        'bootstrap.servers': "localhost:9092",
        'group.id': 'text2image_consumer_group',
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False  # Disable auto-commit
    }

    # Create the consumer
    consumer = Consumer(consumer_config)

    # Subscribe to the topic
    consumer.subscribe(['text2image'])

    try:
        logger.info('Starting consumer')
        while True:
            # Poll for messages
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info('Reached end of partition')
                else:
                    logger.error(f'Error: {msg.error()}')
            else:
                # Process the message
                try:
                    message_data = json.loads(msg.value().decode('utf-8'))
                    logger.info(f'Received message: {message_data}')
                    
                    # Process the message here (e.g., generate image from prompt)
                    # ...
                    text2image_task(db, message_data)

                    # Manually commit the offset to mark the message as processed and delete it
                    consumer.commit(msg)
                    logger.info(f'Processed and committed message: {message_data}')
                except json.JSONDecodeError:
                    logger.error(f'Failed to decode message: {msg.value()}')
                except Exception as e:
                    logger.error(f'Error processing message: {str(e)}')

    except KeyboardInterrupt:
        logger.info('Consumer stopped by user')
    finally:
        logger.info('Closing consumer')
        # Close the consumer
        consumer.close()



def update_task(db, id, image_path):
    collection = db['text2image']
    result = collection.find_one({'_id': ObjectId(id)})
    # write the name of the image to the database
    collection.update_one({'_id': ObjectId(id)}, {'$set': {'image': image_path}})
    
    return result


def text2image_task(db, data):
    # Load the model in fp32 precision (default for CPU)
    pipe = AmusedPipeline.from_pretrained(
        "amused/amused-256", torch_dtype=torch.float32
    )

    # Move the model to CPU
    pipe = pipe.to("cpu")

    # Define the prompt and negative prompt
    # prompt = "A mecha robot in a favela in expressionist style, with a sunset in the background"
    prompt = data['prompt_text']
    negative_prompt = ""

    # Generate the image on CPU
    image = pipe(prompt, negative_prompt=negative_prompt, generator=torch.manual_seed(0)).images[0]

    # Display or return the image
    image_path = f"{data['task_id']}.png"
    image.save("static/images/" + image_path)

    update_task(db, data['task_id'], image_path)

