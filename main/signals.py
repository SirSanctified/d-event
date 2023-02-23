import os

from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from main.models import Participant


@receiver(post_save, sender=User)
def create_participant_profile(sender, instance, created, **kwargs):
    if created:
        Participant.objects.create(attendant=instance)
        user_group = Group.objects.get(name='participant')
        instance.groups.add(user_group)
        send_mail(
            from_email=os.getenv('EMAIL_USER'),
            subject='Welcome to D-Event',
            message=f"""Hello {instance.first_name},\n\n
            Thank you for registering to D-Event.\n
            We Are Excited To Have You Join Us For An Engaging And Inspiring Experience.\n
            We hope you enjoy your stay.\n\n
            Best regards,\n
            D-Event Team""",
            recipient_list=[instance.email],
            fail_silently=False,
        )


@receiver(post_delete, sender=Participant)
def participant_post_delete(sender, instance, **kwargs):
    user = instance.attendant
    send_mail(
        from_email=os.getenv('EMAIL_USER'),
        subject='Thank you for your time with us',
        message=f"""Hello {user.first_name},\n\n
                Thank you for trying out D-Event.\n
                We, however, regret seeing you leave. If there's anything you suggest we improve, please let us know.\n
                We hope to see you again next time.\n\n
                Best regards,\n
                D-Event Team""",
        recipient_list=[user.email],
        fail_silently=False,
    )
    user.delete()
