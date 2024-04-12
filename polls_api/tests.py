from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

# Serializer Test
class VoteSerializerTest(TestCase):
    # setUp 메서드는 각 테스트에 공통부분을 작성해서 일괄적으로 적용시키는 함수이다.
    # setUp을 이용한 결과는 다음 테스트에 반영되지 않는다. 
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.question = Question.objects.create(
            question_text = 'abc',
            owner = self.user
        )

        self.choice = Choice.objects.create(
            question = self.question,
            choice_text = '1',
        )        

    def test_with_valid_data(self):
        data = {
            'question' : self.question.id,
            'choice' : self.choice.id,
            'voter' : self.user.id,            
        }

        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        vote = serializer.save()
        
        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self.user)
    
    def test_vote_serializer_with_duplicate_vote(self):
        choice1 = Choice.objects.create(
            question = self.question,
            choice_text = '2',
        )

        Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)

        data = {
            'question' : self.question.id,
            'choice' : choice1.id,
            'voter' : self.user.id,            
        }

        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_vote_serializer_with_unmatched_question_and_choice(self):
        question2 = Question.objects.create(
            question_text = 'abc',
            owner = self.user
        )

        choice2 = Choice.objects.create(
            question = question2,
            choice_text = '1',
        )  

        data = {
            'question' : self.question.id,
            'choice' : choice2.id,
            'voter' : self.user.id,            
        }
        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        
# Serializer Test
class QuestionSerializerTestCase(TestCase):
    def test_with_valid_data(self):
        serializer = QuestionSerializer(data={'question_text': 'abc'})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)
        
    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data={'question_text': ''})
        self.assertEqual(serializer.is_valid(), False)


# View Test
class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {'question_text': 'some question'}
        self.url = reverse('question-list')
    
    def test_create_question(self):
        user =User.objects.create(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.question_text, self.question_data['question_text'])
        self.assertLess((timezone.now() - question.pub_date).total_seconds(), 1)
    
    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
 
    def test_list_question(self):
        question = Question.objects.create(question_text='Question1')
        choice = Choice.objects.create(question=question, choice_text='Question1')
        Question.objects.create(question_text='Question2')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['choices'][0]['choice_text'], choice.choice_text)