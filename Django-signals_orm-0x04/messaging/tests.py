from django.test import TestCase
from .models import Message

class MessageModelTest(TestCase):
    def test_create_message(self):
        msg = Message.objects.create(
            sender='Alice',
            receiver='Bob',
            content='Hello Bob!'
        )
        self.assertEqual(str(msg), 'From Alice to Bob')
