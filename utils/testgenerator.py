import json
import os
from pathlib import Path
from random import randint, shuffle
from pprint import pprint
import pandas as pd


class TestGenerator:

    def __init__(self, variants, test_id, is_random=True, random_variants=True, ):
        self.is_random = is_random
        self.random_variants = random_variants
        self.number_of_variants = variants
        self.test_id = test_id
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.keys = ['A','B','C','D']
    def files_to_test(self, files: dict):
        try:
            full_data = []
            for _ in range(self.number_of_variants):
                quizzes = []
                for file, number_of_tests in files.items():
                    quiz = self.generate_test(self.read_data(file, number_of_tests))
                    # pprint(quiz)
                    quizzes.extend(quiz)
                answers = []
                full_data.append(dict())
                full_data[_]= dict()
                full_data[_]['questions'] = quizzes
                questions =full_data[_]['questions']
                shuffle(questions)
                for element in questions:
                    answers.append(self.keys[element['correct_ans']])
                full_data[_]['answers'] = answers
            self.dump_tests(full_data)
            return full_data
        except Exception as e:
            print("Error : ", e)

    # @staticmethod
    def read_data(self, filename: str, number_quizzes: int, ) -> dict:
        questions = dict()
        try:
            test_file = self.BASE_DIR / 'files' / self.test_id /filename
            tests = pd.read_excel(test_file)
            quizzes = list(tests['question'].tolist())
            num_quizzes = len(quizzes)
            quizzes_list2 = quizzes[::]
            for i in range(0, number_quizzes):
                random_quiz_number = randint(0, num_quizzes - 1) if self.is_random else i
                quiz = quizzes[random_quiz_number]
                questions[quiz] = dict()
                quizzes.remove(quiz)
                for j in ['A', 'B', 'C', 'D']:
                    questions[quiz][j] = tests[j].tolist()[quizzes_list2.index(quiz)]
                if self.is_random:
                    num_quizzes -= 1
            return questions
        except Exception as e:
            print("ERROR:", e)
            return questions

    def generate_test(self, quizzes: dict, ):
        try:
            new_quizzes = []
            ln = len(quizzes)
            q_variants = ['A', 'B', 'C', 'D']
            quizzes_list = list(quizzes.keys())

            for i in range(ln):
                if self.random_variants:
                    shuffle(q_variants)
                quiz = quizzes_list[i]
                new_quizzes.append(dict())
                new_quizzes[i]['text'] = quiz
                new_quizzes[i]['keys'] = []
                for j in q_variants:
                    new_quizzes[i]['keys'].append(quizzes[quiz][j])
                new_quizzes[i]['correct_ans'] = q_variants.index('A')
            return new_quizzes
        except Exception as e:
            print("ERROR(correct_ans):", e.args)

    def dump_tests(self, writing_data):
        try:
            url = self.BASE_DIR / 'tests' / (self.test_id + '.json')
            if os.path.exists(url):
                print(url)
                return False
            json_object = json.dumps(writing_data, indent=4)
            print(json_object)
            with open(url, 'w') as f:
                f.write(json_object)
            return True
        except Exception as e:
            print("ERROR: ", e)
if __name__ == '__main__':
    gen = TestGenerator(3, '0002')
    data = gen.files_to_test({'test2.xlsx':20,})
    gen.dump_tests(data)
