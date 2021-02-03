import time

import cv2
import numpy as np
import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from nothotdog.photos.models import Photo
from tensorflow import keras
from skimage import exposure


class Command(BaseCommand):
    help = 'Listens to detect uploads made to the server.'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
        )
        channel = connection.channel()

        channel.queue_declare(queue='hotdog_alert')

        model_path = str(settings.BASE_DIR) + '/nothotdog/photos/hotdog_finder/hotdog_CNN_model'
        model = keras.models.load_model(model_path)

        def callback(ch, method, properties, body):
            photo_id = int.from_bytes(body, byteorder='big')

            # Give time for database to update before accessing.
            time.sleep(1)
            photo = Photo.objects.get(id=photo_id)
            print(f" [x] Processing {photo}.")

            prediction, is_hotdog = process_image(photo)
            hotdog_probability = round(prediction[0] * 100, 1)
            if not is_hotdog:
                photo.flagged = True
                print(f" [x] Flagged {photo}.")

            photo.save()
            print(f" [x] Finished processing {photo}.")
            print(f" [x] Probability of hot dog is {hotdog_probability} %.")

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

            prediction = model.predict(X_normalized)[0]  # First element hot dog, second element not hot dog.
            is_hotdog = True if prediction[0] > prediction[1] else False

            return (prediction, is_hotdog)

        def to_gray(image):
            # rgb2gray converts RGB values to grayscale values by forming a weighted sum of the R, G, and B components:
            # 0.2989 * R + 0.5870 * G + 0.1140 * B
            # source: https://www.mathworks.com/help/matlab/ref/rgb2gray.html

            image = 0.2989*image[:, :, :, 0] + 0.5870*image[:, :, :, 1] + 0.1140*image[:, :, :, 2]
            return image

        def normalize_images(image):
            # use Histogram equalization to get a better range
            # source http://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.equalize_hist
            image = (image / 255.).astype(np.float32)

            for i in range(image.shape[0]):
                image[i] = exposure.equalize_hist(image[i])

            image = image.reshape(image.shape + (1,))
            return image

        channel.basic_consume(
            queue='hotdog_alert',
            on_message_callback=callback,
            auto_ack=True,
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
