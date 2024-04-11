from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from polls.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date')