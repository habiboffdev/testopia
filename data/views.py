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


# This function is not for requests, it is custom made
def create_question(json, test:TestModel):
    questions = json[0]['questions']
    for question in questions:
        questionModel = Question(text=question['text'],options=len(question['keys']),points=1)
        questionModel.save()
        for index,option in enumerate(question['keys']):
            choice = Choice(text=option,is_correct=(question['correct_ans'] == index),question=questionModel)
            choice.save()
        questionModel.save()
        test.questions.add(questionModel)
        test.save()
@login_required
def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        data = request.POST
        if form.is_valid():
            try:
                file = request.FILES['file']
                file_path = os.path.join('D:\\PycharmProjects\\Loyiha-1\\data', file.name)
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
