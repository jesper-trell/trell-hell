import pathlib
import struct
import time

import cv2
import numpy as np
import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from nothotdog.photos.models import Photo
from tensorflow import keras


class Command(BaseCommand):
    help = 'Listens to detect uploads made to the server.'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        channel = connection.channel()

        channel.queue_declare(queue='hotdog_alert')

        def callback(ch, method, properties, body):
            photo_id, created = struct.unpack("i?", body)

            # Do nothing if there was no new upload.
            if not created:
                return

            # Give time for database to update before accessing.
            time.sleep(1)
            photo = Photo.objects.get(id=photo_id)
            print(f" [x] Processing {photo}.")

            # is_hotdog = 'hotdog' in photo.title.lower()
            prediction, is_hotdog = process_image(photo)
            hotdog_probability = round(prediction[1] * 100, 1)
            if not is_hotdog:
                photo.flagged = True
                print(f" [x] Flagged {photo}.")

            photo.description += f" ({hotdog_probability} %)"
            photo.save()
            print(f" [x] Finished processing {photo}.")
            print(f" [x] Probability of hot dog is {hotdog_probability} %.")

        def process_image(photo):
            model_path = str(settings.BASE_DIR) + '/nothotdog/photos/hotdog_finder/hotdog_CNN_model'
            model = keras.models.load_model(model_path)

            img_width, img_height = 25, 25  # 25, 25
            img_path = str(settings.BASE_DIR) + photo.image.url
            read_image = cv2.imread(img_path, 0)  # 0 for grayscale.
            resized_image = cv2.resize(read_image, (img_width, img_height))  # Resizes image.
            reshaped_image = [resized_image]  # Setting correct shape.
            numpy_image = np.array(reshaped_image)
            input_image = numpy_image.reshape((numpy_image.shape[0], img_width, img_height, 1))

            prediction = model.predict(input_image)[0]  # First element not hot dog, second element hot dog.
            is_hotdog = True if prediction[1] > prediction[0] else False

            return (prediction, is_hotdog)

        channel.basic_consume(
            queue='hotdog_alert',
            on_message_callback=callback,
            auto_ack=True,
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
