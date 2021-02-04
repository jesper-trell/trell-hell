import time

import cv2
import numpy as np
import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from hotdog_finder.data_augmentation import normalize_images, to_gray
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

        model = keras.models.load_model(settings.ML_MODEL_PATH)

        def callback(ch, method, properties, body):
            photo_id = int.from_bytes(body, byteorder='big')

            # Give time for database to update before accessing.
            time.sleep(1)
            photo = Photo.objects.get(id=photo_id)
            print(f' [x] Processing {photo}.')

            prediction, is_hotdog = process_image(photo)
            hotdog_probability = round(prediction[0] * 100, 1)
            if not is_hotdog:
                photo.flagged = True
                print(f' [x] Flagged {photo}.')

            photo.save()
            print(f' [x] Finished processing {photo}.')
            print(f' [x] Probability of hot dog is {hotdog_probability} %.')

        def process_image(photo):
            img_size = (32, 32)
            img_path = str(settings.BASE_DIR) + photo.image.url
            read_image = cv2.imread(img_path)
            resized_image = cv2.resize(read_image, img_size)
            X_array = np.array(resized_image)
            X_resized = X_array.reshape(
                            1,
                            X_array.shape[0],
                            X_array.shape[1],
                            X_array.shape[2],
                            )

            X_gray = to_gray(X_resized)
            X_normalized = normalize_images(X_gray)

            # First element hot dog, second element not hot dog.
            prediction = model.predict(X_normalized)[0]
            is_hotdog = True if prediction[0] > prediction[1] else False

            return (prediction, is_hotdog)

        channel.basic_consume(
            queue='hotdog_alert',
            on_message_callback=callback,
            auto_ack=True,
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
