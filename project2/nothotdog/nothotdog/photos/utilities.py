from django.core.mail import send_mail


def send_like_mail(like):
    send_mail(
            subject='Photo Liked',
            message=(
                f'The image "{like.photo}" has been liked '
                + f'by the user "{like.user}".'
            ),
            from_email='info@trell.se',
            recipient_list=[like.user.email],

            fail_silently=False,
    )


def send_flag_mail(photo):
    send_mail(
            subject='Photo Flagged',
            message=(
                f'The image "{photo}" has been flagged '
                + 'for not depicting a hot dog.'
            ),
            from_email='info@trell.se',
            recipient_list=[photo.user.email],
            fail_silently=False,
    )
