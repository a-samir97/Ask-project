from django.db import models
from accounts.models import Account

class Question(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='asked')
    body = models.TextField()
    to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='answered')
    is_answered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} || {} ...".format(self.author.username,self.body[:10])

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} || {}'.format(self.author.username, self.body[:10])
