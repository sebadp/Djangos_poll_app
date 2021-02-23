from django.test import TestCase
import datetime
from django.utils import timezone
from polls.models import Question
from django.urls import reverse

def create_question(question_text, days):
    """
    Crea una Question con los argumentos que le pasamos a la función
    si la queremos en el pasado o en el futuro lo determinamos con el 
    segundo argumento, days, en positivo o negativo.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        Was_published_recently() Tendría que retornar falso
        cuando se crea una Question con pub_date en el futuro.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        Tendría que retornar falso si creamos una Question de más de un día.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        Tendría que retornar True si creamos una Question dentro del rango de un día
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Si no existe una Question, un mensaje apropiado se debería presentar
        """
        response = self.client.get(reverse('polls:index'))
        print(response.context)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay Encuestas disponibles")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Una Question en el pasado se tendría que mostrar en el index
        """
        create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_test_future_question(self):
        """
        Las Question en futuro no se deberían mostrar en index
        """
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No hay Encuestas disponibles")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Habiendo Questions tanto en pasado como en futuro, sólo las pasadas se tienen que publicar
        """
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_questions(self):
        """
        Probamos que si hay varias Question en pasado, se muestren todas
        """
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        El detalle de una Question que está en el futuro tendría que responder
        un 404 Not Found
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        El detalle de una Question en el pasado tiene que mostrar el texto de la Question
        """
        past_question = create_question(question_text='Past question.', days=-5)
        url= reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
