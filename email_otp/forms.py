from django.forms import Form, CharField


class EmailForm(Form):
    email = CharField(max_length=255)
