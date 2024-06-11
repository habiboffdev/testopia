import uuid

from django.db import models
from django.db.models import OneToOneField

from core.models import User
# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=500,null=True,blank=True)
    point = models.FloatField(default=1.0)
    options = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    is_multiple_choice = models.BooleanField(default=False)
    def __str__(self):
        return self.text
class TestModel(models.Model):
    name = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,blank=True,null=True)
    count = models.IntegerField(default=0)
    isRandom = models.BooleanField(default=True)
    isVariantsRandom = models.BooleanField(default=True)
    isRated = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    questions = models.ManyToManyField(Question, blank=True)
    full_mark = models.FloatField(default=0)
    
    
    def __str__(self):
        return f"{self.name}"
    def delete(self, *args, **kwargs):
        # Delete related models
        print("Deleted...")
        # self.related_models.clear()  # This will remove the relationship but not delete the related objects
        # If you want to delete the related objects, you can do it like this:
        for related in self.questions.all():
            related.delete()
        super(TestModel, self).delete(*args, **kwargs)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=500,null=True,blank=True)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.text


class UserChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question: {self.question.id}, Choice: {self.choice.text}"
    
class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    started_time = models.DateTimeField(auto_now_add=True)
    ended_time = models.DateTimeField(auto_now_add=False,null=True,blank=True)
    def __str__(self):
        return f"{self.user.username}-{self.quiz}"
    class Meta:
        verbose_name_plural = "User Tests"
class OngoingTests(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quiz = models.OneToOneField(TestModel, on_delete=models.CASCADE)
    started_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.quiz}"
    class Meta:
        verbose_name_plural = "Ongoing Tests"



class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.ManyToManyField(UserChoice)
    quiz = models.ForeignKey(TestModel, on_delete=models.CASCADE)
    cached_test = models.ForeignKey(UserTest, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"{self.user.username}"
    class Meta:
        verbose_name_plural = "User Answers"











