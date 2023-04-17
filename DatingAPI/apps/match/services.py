from apps.match.models import Match
from django.conf import settings
from django.core.mail import send_mail


class Matching:

    @staticmethod
    def is_mutually(valuer, expectant):
        expectant_match_list = Match.objects.filter(valuer=expectant)
        return any([match.expectant == valuer for match in expectant_match_list])

    @staticmethod
    def send_info_if_mutually(user, expectant, mark, data, new_data=None):
        """
        If user likes expectant and expectant likes user,
        user will see expectant email and email will be sent to both
        """
        if new_data is None:
            new_data = {}
            new_data.update(data)
        if mark and Matching.is_mutually(user, expectant):
            new_data.update({'expectant_email': expectant.email})
            Matching.send_notification(user, expectant)
            # Mail detected like spam and error raises.
            # I do not want to use another mail hosting because they ask my telephone number when registration.
            # And I do not want to use my own account.
        return new_data

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

