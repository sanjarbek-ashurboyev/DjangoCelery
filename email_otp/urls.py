from django.urls import path

from email_otp.views import EmailFormView, CodeTemplateView

urlpatterns = [
    path('email', EmailFormView.as_view(), name='email'),
    path('code', CodeTemplateView.as_view(), name='code'),

]