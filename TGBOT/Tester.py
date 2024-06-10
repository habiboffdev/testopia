import logging

from telebot import TeleBot

from telebot.types import Message, CallbackQuery
from .buttons import gentest_markup, genlist_markup, remove_markup
from .testModel import QuizUtil
from core.models import User
from data.models import Question
from random import randint
from time import time,sleep


class Test:
    def __init__(self, bot: TeleBot, chat_id: int, test_number: int):
        self.bot = bot
        self.chat_id = chat_id
        self.user = User.get(uid=chat_id)
        self.test_number = test_number
        self.start_time = time()
        self.callback_handler = self.bot.callback_query_handler
        self.variant = randint(1, 1)
        self.testData: QuizUtil = QuizUtil(test_number, self.user)
        self.question: Question = self.testData.get_question()
        self.markup = gentest_markup(self.testData)
    def start(self):
        try:
            self.start_time = time()

            self.bot.send_message(self.chat_id, "<i>⏰Test 3 sekundda boshlanadi...</i>",parse_mode='HTML')

            sleep(3)
            self.bot.send_message(self.chat_id, f"Test boshlandi\nJami savollar:  {self.testData.number_of_questions}\nVariant: {self.variant}",
                             reply_markup=remove_markup())
            self.bot.send_message(self.chat_id, self.question.text, reply_markup=self.markup, parse_mode="HTML")
        except Exception as e:
            logging.error(e)
    def new_test(self,msg: Message):
        self.question = self.testData.get_question()
        self.bot.edit_message_text(self.question.text, msg.chat.id, msg.id,
                              reply_markup=gentest_markup(self.testData), parse_mode="HTML")
    # For using callback_handler
    def check_test(self,callback: CallbackQuery):
        try:
            resp = callback.data
            msg = callback.message
            quiz = self.testData.data[self.testData.current_question]
            if resp == "back":
                pass
            elif resp == "skip":
                self.new_test(msg)
            elif resp.startswith("next"):
                self.new_test(msg)
            elif resp.isdigit():
                self.testData.tick_answer(int(resp))
                self.bot.edit_message_text(quiz["text"], msg.chat.id, msg.id,
                                      reply_markup=gentest_markup(self.testData), parse_mode="HTML")
            elif resp == "finish":

                self.bot.delete_message(msg.chat.id, msg.id)
                self.bot.send_message(msg.chat.id, "Natija: " + str(self.testData.get_result()) + "/" + str(self.testData.number_of_questions))
                return 1
            return 0

        except Exception as e:
            logging.error(e)