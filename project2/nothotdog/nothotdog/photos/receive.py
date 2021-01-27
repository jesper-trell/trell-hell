import pika, sys, os

import django
from django.conf import settings
from models import Photo
# from nothotdog.photos import model


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hotdog_alert')

    def callback(ch, method, properties, body):
        # photo = Photo.objects.get(hashid=photo_hashid)
        print(" [x] Received %r" % body)


    channel.basic_consume(queue='hotdog_alert', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
