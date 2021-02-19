from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        Was_published_recently() Tendría que retornar falso
        cuando se crea una Question con pub_date en el futuro.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)