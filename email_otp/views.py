import random


from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from redis import Redis

from email_otp.forms import EmailForm
from email_otp.tasks import send_mail


# Create your views here.
class EmailFormView(FormView):
    template_name = 'email.html'
    form_class = EmailForm
    success_url = reverse_lazy('code')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        code = random.randint(100000, 999999)

        send_mail.delay(email, code)
        rd = Redis(host='localhost', port=6379, db=1, decode_responses=True)
        rd.set(email,code)
        return super().form_valid(form)

    def form_invalid(self, form):
        pass

class CodeTemplateView(TemplateView):
    template_name = 'otp-code.html'