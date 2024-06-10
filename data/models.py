import uuid

from django.db import models
from django.db.models import OneToOneField

from core.models import User
# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=500,null=True,blank=True)
    points = models.FloatField(default=1.0)
    options = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}, Question: {self.question.text}, Choice: {self.choice.text}"

class OngoingTests(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quiz = models.OneToOneField(TestModel, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.quiz}"
    class Meta:
        verbose_name_plural = "Ongoing Tests"











