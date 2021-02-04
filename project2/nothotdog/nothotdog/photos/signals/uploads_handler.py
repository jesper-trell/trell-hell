import pika
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from nothotdog.photos.models import Photo


@receiver(post_save, sender=Photo)
def upload_handler(sender, instance, created, **kwargs):
    # Do nothing if there was no new upload.
    if created:
        bytes_data = (instance.id).to_bytes(2, byteorder='big')
        send_photo_alert(bytes_data)


def send_photo_alert(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue='hotdog_alert')
    channel.basic_publish(
        exchange='',
        routing_key='hotdog_alert',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent.
        )
    )
    connection.close()
