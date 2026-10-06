import secrets

from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from redis import Redis

from email_otp.forms import EmailForm
from email_otp.tasks import send_mail

# Matches the 10:00 countdown on the code page.
OTP_TTL_SECONDS = 600


def redis_client():
    return Redis(host='localhost', port=6379, db=1, decode_responses=True)


class EmailFormView(FormView):
    template_name = 'email.html'
    form_class = EmailForm
    success_url = reverse_lazy('code')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        # secrets, not random: one-time codes must not be predictable.
        code = f'{secrets.randbelow(1_000_000):06d}'

        # Store the code before queuing the email, so it already exists when the user reads it.
        redis_client().set(f'otp:{email}', code, ex=OTP_TTL_SECONDS)
        send_mail.delay(email, code)
        return super().form_valid(form)


class CodeTemplateView(TemplateView):
    template_name = 'otp-code.html'
