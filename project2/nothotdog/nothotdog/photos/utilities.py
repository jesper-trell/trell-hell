from django.core.mail import send_mail


def send_alert_mail(like=None, photo=None):
    if like:
        subject = 'Image Liked'
        message = (
            f'The image "{like.photo}" has been liked '
            + f'by the user "{like.user}".'
        )
        recipient_list = [like.user.email]
    elif photo:
        subject = 'Image Flagged'
        message = (
            f'The image "{photo}" has been flagged '
            + 'for not depicting a hot dog.'
        )
        recipient_list = [photo.user.email]

    send_mail(
            subject=subject,
            message=message,
            from_email='info@trell.se',
            recipient_list=recipient_list,
            fail_silently=False,
    )
