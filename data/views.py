# Create your views here.
# Django
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import TestModel, Question, Choice
# Other
import os
import logging
import pandas as pd

# Utils
from utils.testgenerator import TestGenerator
from .forms import UploadFileForm
from json import dumps

# This function is not for requests, it is custom made
def create_question(json, test:TestModel):
    questions = json[0]['questions']
    cnt = 1
    sum_of_points: float = 0
    for question in questions:
        questionModel = Question(text=question['text'],options=len(question['keys']),order=cnt)
        questionModel.save()
        for index,option in enumerate(question['keys']):
            choice = Choice(text=option,is_correct=(question['correct_ans'] == index),question=questionModel) # Creating Choice
            choice.save()
        questionModel.point = question['point'] # Adding point
        questionModel.save()
        test.questions.add(questionModel)
        cnt+=1
        sum_of_points+=questionModel.point # sum of points
    test.full_mark = sum_of_points
    test.save()
@login_required
def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        data = request.POST
        if form.is_valid():
            try:
                file = request.FILES['file']
                file_path = os.path.join('D:\\PycharmProjects\\Loyiha-1\\files', file.name)
                with open(file_path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                test = TestModel(user=request.user,name=request.POST['title'],description=request.POST['description'],count=request.POST['count'])
                test.save()
                generator = TestGenerator(1, str(test.uid))
                data = generator.files_to_test({file_path: int(request.POST['count']), })
                generator.dump_tests(data)
                create_question(data,test)
                excel_file = pd.read_excel(file_path)

                return render(request, 'success.html', {'excel_data': excel_file.to_html()})
            except Exception as e:
                logging.error(e)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
def solve_test(request,id):
    try:
        test = TestModel.objects.get(id=id)
        questions = test.questions.all()
        question_list = list(questions.values())
        choices = dict()
        for index in range(questions.__len__()):
            choices[index] = list(Choice.objects.filter(question=questions[index]).values_list('text', flat=True))
        # print(questions)
        # print(choices)
        return render(request, 'test.html', {'data': test, 'questions': dumps(question_list),'choices':dumps(choices)})
    except Exception as e:
        logging.error(e)