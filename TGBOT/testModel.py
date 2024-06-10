import time
from data.models import TestModel, UserAnswer, UserChoice, Question, UserTest
from core.models import User
from .readJson import readjson
class QuizUtil:
    def __init__(self,test_id , user:User):
        self.data = TestModel.objects.get(id=test_id)
        self.answers = UserAnswer(user=user,quiz=self.data)
        self.answers.save()
        self.time = 0
        self.user = user
        self.number_of_questions = self.data.questions.count()
        self.answers = {i : -1 for i in range(self.number_of_questions)}
        self.current_question : Question = None
        self.current_question_number : int = -1
        self.result = {i : {"Correct" : i, "Your ans": i} for i in range(self.number_of_questions)}
        self.user_test: UserTest = UserTest(user=user,quiz=self.data)
        self.user_test.save()
    def tick_answer(self, answer):
        try:
            # send to back_end(soon)
            choice = UserChoice(question = self.current_question, choice=answer)
            choice.save()
            if self.answers.objects.filter(question=self.current_question).exists() and not self.current_question.is_multiple_choice:
                self.answers.choices.filter(question=self.current_question).delete()
            else:
                self.answers.choices.add(choice)
        except Exception as e:
            print("ERROR(tick_answer): ", e)
    def get_checked(self):
        try:
            cnt = 0
            for answer in self.answers.values():
                if answer == "skipped":
                    continue
                if answer>=0:
                    cnt+=1
            return cnt
        except Exception as e:
            print("ERROR(get_checked): ", e)
    def get_question(self)->list:
        try:
            self.current_question_number += 1
            if self.current_question_number == self.number_of_questions:
                self.current_question_number = 0
            self.current_question = self.data.questions.all().get(number=self.current_question_number)
            return self.current_question
        except Exception as e:
                print("ERROR(get_question): ", e)
    def get_result(self):
        self.user_test.ended_time = time.time()
        correct_ans = 0
        incorrect_ans = 0
        points = 0
        for choice in self.answers.choices.all():
            if choice.is_correct:
                correct_ans += 1
                points += choice.question.points
            else:
                incorrect_ans += 1
        self.user_test.correct = correct_ans
        self.user_test.incorrect = incorrect_ans
        self.user_test.total = points
        self.user_test.save()
        return points

def read_beta(variant,id):
    data = readjson(f"{id}.json")
    test = 0
    return test
