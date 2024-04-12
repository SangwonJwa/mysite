from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.was_published_recently():
            new_badge = "NEW!!!"
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}'
    
    @admin.display(boolean=True, description='최근 생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    # 하나의 question에 대해 사용자는 하나의 vote만 가질 수 있게 설정.
    class Meta:
        constraints =[
            models.UniqueConstraint(fields=['question', 'voter'], name='unique_voter_for_questions'),
        ]



# Create your models here.
