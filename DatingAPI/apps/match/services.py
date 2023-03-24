from apps.match.models import Match
from django.conf import settings
from django.core.mail import send_mail


class Matching:

    @staticmethod
    def is_mutually(valuer, expectant):
        expectant_match_list = Match.objects.filter(valuer=expectant)
        return any([match.expectant == valuer for match in expectant_match_list])

    @staticmethod
    def send_notification(valuer, expectant):
        subject = 'You have match!'
        email_from = settings.EMAIL_HOST_USER
        message = f'Hello {valuer.username}!\nYou just had a match! ' \
                  f'You are liked {expectant.first_name}. Your soulmate email: {expectant.email}'
        send_mail(subject, message, email_from, [valuer.email])
        message = f'Hello {expectant.username}!\nYou just had a match! ' \
                  f'You are liked {valuer.first_name}. Your soulmate email: {valuer.email}'
        send_mail(subject, message, email_from, [expectant.email])

