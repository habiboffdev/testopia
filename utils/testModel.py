import time

from .readJson import readjson
class Test:
    def __init__(self,data):
        self.data = data
        self.time = 0
        self.number_of_questions = len(data)
        self.answers = {i : -1 for i in range(self.number_of_questions)}
        self.current_question = -1
        self.result = {i : {"Correct" : i, "Your ans": i} for i in range(self.number_of_questions)}
        self.started_time = -1
        self.end_time = -1

    def check_time(self):
        try:
            delta = time.time()-self.started_time
            if delta>self.time:
                return -1
            else:
                return self.time- delta
        except Exception as e:
            print("Error(Chekc_time):",e)
    def tick_answer(self, answer):
        try:
            # send to back_end(soon)
            self.answers[self.current_question] = answer
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
    def get_question(self):
        try:
            self.current_question += 1
            if self.current_question == self.number_of_questions:
                self.current_question = 0
            return self.data[self.current_question]
        except Exception as e:
                print("ERROR(get_question): ", e)
    def get_result(self):
        correct_ans = 0
        for q,ans in self.answers.items():
            if self.data[q]["correct_ans"] == ans:
                correct_ans += 1
        return correct_ans

def read_beta(variant,id):
    data = readjson(f"{id}.json")
    test = Test(data[variant-1]['questions'])
    test.time = data[variant-1]["time"]
    return test
