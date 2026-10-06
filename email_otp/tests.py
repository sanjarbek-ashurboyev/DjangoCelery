from unittest import mock

from django.test import TestCase
from django.urls import reverse

from email_otp.views import OTP_TTL_SECONDS


@mock.patch('email_otp.views.send_mail')
@mock.patch('email_otp.views.redis_client')
class EmailFormViewTests(TestCase):
    def test_valid_email_stores_code_with_expiry_and_queues_email(self, redis_client, send_mail):
        response = self.client.post(reverse('email'), {'email': 'user@example.com'})

        self.assertRedirects(response, reverse('code'), fetch_redirect_response=False)
        key, code = redis_client.return_value.set.call_args.args
        self.assertEqual(key, 'otp:user@example.com')
        self.assertEqual(redis_client.return_value.set.call_args.kwargs, {'ex': OTP_TTL_SECONDS})
        self.assertRegex(code, r'^\d{6}$')
        send_mail.delay.assert_called_once_with('user@example.com', code)

    def test_invalid_email_shows_form_error_and_sends_nothing(self, redis_client, send_mail):
        response = self.client.post(reverse('email'), {'email': 'not-an-email'})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertContains(response, 'style="display: block"')
        redis_client.return_value.set.assert_not_called()
        send_mail.delay.assert_not_called()

    def test_codes_are_not_repeated(self, redis_client, send_mail):
        for _ in range(20):
            self.client.post(reverse('email'), {'email': 'user@example.com'})
        codes = {c.args[1] for c in redis_client.return_value.set.call_args_list}
        self.assertGreater(len(codes), 15)
