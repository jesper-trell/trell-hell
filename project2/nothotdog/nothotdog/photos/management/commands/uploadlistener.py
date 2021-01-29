import struct
import time

import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from nothotdog.photos.models import Photo


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
            time.sleep(1)
            photo = Photo.objects.get(id=photo_id)
            print(f" [x] Processing {photo}.")

            is_hotdog = 'hotdog' in photo.title.lower()
            if not is_hotdog and created:
                photo.flagged = True
                photo.save()
                print(f" [x] Flagged {photo}.")

        channel.basic_consume(
            queue='hotdog_alert',
            on_message_callback=callback,
            auto_ack=True,
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
