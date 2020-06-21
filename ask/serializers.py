from rest_framework import serializers
from .models import Question, Answer

from accounts.serializers import AccountShowSerializer

class QuestionSerializer(serializers.ModelSerializer):
    author = AccountShowSerializer()
    class Meta:
        model = Question
        exclude = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    author = AccountShowSerializer()
    class Meta:
        model = Answer
        exclude = ('id',)
