from django.forms import Form, EmailField


class EmailForm(Form):
    email = EmailField(max_length=255)
