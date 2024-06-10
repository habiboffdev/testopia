from utils.testgenerator import TestGenerator
from random import randint
import json


number_of_files = int(input("Nechta fayl bor? "))
number_of_variants = int(input('Nechta variant qimoqchisiz? '))
data = dict()
for _ in range(number_of_files):
    name = input('File nomi: ')
    number_of_tests = int(input(name + ' faylidan nechta test olish kerak? '))
    data[name] = number_of_tests
test_id = input('Testning id raqamini kiriting(ex. 0001) : ')
generator = TestGenerator(number_of_variants,test_id)
new_data = generator.files_to_test(data)

temp = int(input('Misol yechishni xoxlaysizmi? '))
if temp == 1:
     points = 0
     var = randint(1,number_of_variants)
     questions = new_data[var-1]['questions']
     for i, ques in enumerate(questions):
         print(f"{i+1}) {ques['text']}")
         for j, key in enumerate(ques['keys']):
             print(f"{generator.keys[j]}. {key}")
         answer = input('')
         if answer == generator.keys[ques['correct_ans']]:
             points+=1
     print(points, 'ta to\'g\'ri javob')