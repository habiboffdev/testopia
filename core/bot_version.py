# Django
from django.core.validators import RegexValidator
from django.conf import settings

# Built-in
import json
from typing import List

# Extra
import telebot
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Local
from core.models import User
from utils.decorators import lock_non_registered
from .texts import Texts, Constants
import logging
from TGBOT.buttons import genlist_markup, gentest_markup
from data.models import UserChoice,Question,TestModel, OngoingTests
from TGBOT.BotTest import Test
# from utils.testerCallback import gentest_markup, genlist_markup, remove_markup
# from utils.testModel import read_beta
# import threading
def is_registered(user_id: int, registered_users: List[int] = None):
    """Check if a user is registered.

    Args:
        user_id (int): The user ID to check registration status.
        registered_users (List[int], optional): A list of registered user IDs.
            Defaults to None.

    Returns:
        bool: True if the user is registered, False otherwise.
    """
    if not registered_users:
        registered_users = [settings.DEV_ID]
    return user_id in registered_users or User.objects.filter(uid=user_id).exists()


class Testopia(TeleBot):
    texts = Texts()
    _id = _username = None

    @property
    def id(self):
        # we cache the bot id, since we may need it alot
        if self._id is None:
            self._id = self.get_me().id
        return self._id

    @property
    def username(self):
        if self._username is None:
            self._username = bot.get_me().username
        return self._username

    def set_context(self, message: telebot.types.Message, _key: str, _value) -> None:
        request_id = self.generate_unique_id(message=message)
        if hasattr(self, 'context'):
            self.context[request_id] = {_key: _value}

    @staticmethod
    def generate_unique_id(json_string: str = None, message: Message = None):
        template = '{date}-{chat_id}'
        if json_string:
            json_data = json.loads(json_string)
            msg = json_data[list(json_data.keys())[1]]
            return template.format(
                date=msg["date"], chat_id=msg["chat"]["id"])
        elif message:
            return template.format(date=message.date, chat_id=message.chat.id)
        else:
            raise ValueError("No data to process. Provide at least one of these: json_string, message")

    def notify_register(self, msg: Message):
        try:
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(InlineKeyboardButton(self.texts.register_call_back, callback_data="register"))
            self.send_message(msg.chat.id, self.texts.register, reply_markup=markup)
        except Exception as e:
            logging.error(e)
    def register(self, msg: Message):
        try:
            text = str(msg.text).strip(' ')
            # check the user exist because we need to find step
            step = None
            if not is_registered(msg.from_user.id, []):
                try:
                    user = User(username=text, uid=msg.from_user.id, platform=0)
                    user.save()
                    step = self.send_message(msg.chat.id, self.texts.register_fullname)
                    self.set_next_step(user,Constants.STEP_USERNAME)
                except:
                    step = self.send_message(msg.chat.id, self.texts.register_step_username_wrong)
                finally:
                    bot.register_next_step_handler(step, self.register)
            else:
                user:User = User.get(uid=msg.from_user.id)
                if user.step == Constants.STEP_USERNAME:
                    user.full_name = text
                    user.save()
                    step = self.send_message(msg.chat.id, self.texts.register_age)
                    self.set_next_step(user,Constants.STEP_FULLNAME)
                    bot.register_next_step_handler(step, self.register)
                elif user.step == Constants.STEP_FULLNAME:
                    user.age = int(text)
                    user.save()
                    self.send_message(msg.chat.id, self.texts.register_done)
                    self.set_next_step(user,Constants.STEP_AGE)


        except Exception as e:
            logging.error(e)

    @staticmethod
    def set_next_step(user: User, step: int, temp_data: str = None) -> None:
        user.step = step
        user.temp_data = temp_data if temp_data is not None else user.temp_data
        user.save()
bot = Testopia(token=settings.BOT_TOKEN)


@bot.message_handler(commands=["start"])
@lock_non_registered(checker=is_registered, default=bot.notify_register)
def command_handler(msg: Message):
    text = msg.text
    if len(text.split()) > 1:
        if text.split()[1].startswith('test'):
            test_by_id(msg)
    else:

        bot.send_message(msg.chat.id, bot.texts.welcome)

@bot.callback_query_handler(lambda call: True)
def callback_handler(call: CallbackQuery):
    uid = call.from_user.id
    if call.data == "register":
        try:
            msg = bot.send_message(uid,bot.texts.register_step_username)

            bot.register_next_step_handler(msg, bot.register)
        except Exception as e:
            logging.error(e)
        finally:
            pass
    else:
        try:
            check_test(call)
        except Exception as e:
            logging.error(e)
# @bot.message_handler(commands=['test'])
def test_by_id(msg: Message) -> None:
    """
    This function extracts the test_id from the message text and calls the test_info function.

    Args:
        msg (Message): The incoming message object.

    Returns:
        None
    """
    try:
        text = msg.text
        test_id = text.split('=')[1]
        # Call the test_info function
        test_info(msg,test_id)
    except Exception as e:
        logging.error("ERROR(test_by_id): ", e) # log the error
@bot.message_handler(commands=['tests'])
@lock_non_registered(checker=is_registered, default=bot.notify_register)
def tests_function(msg: Message):
    try:
        objects = list(TestModel.objects.values_list("name","id"))
        objects = [f"{object[1]}-{object[0]}" for object in objects]
        mark = genlist_markup(list(objects))
        bot.reply_to(msg, "📄Quyidagi testlardan birini tanlang👇", reply_markup=mark)
        bot.register_next_step_handler(msg, test_info)
    except Exception as e:
        print("ERROR(tests_function): ", e)
ongoing_tests = dict()
def test_info(msg : Message, test_id: str = None):
    try:
        test_id = test_id if test_id is not None else msg.text.split('-')[0]
        if OngoingTests.objects.filter(user=User.get(uid=msg.chat.id)).first() is not None:
            bot.send_message(msg.chat.id,Texts.have_already_started, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Testga o'tish",callback_data="restart_test-"+test_id)))
            return
        test_model = TestModel.objects.get(id=test_id)
        test_description = test_model.description
        test_number_of_questions = test_model.count
        test_full_mark = test_model.full_mark
        test_name = test_model.name
        bot.send_message(msg.chat.id,Texts.test_info.format(test_name=test_name,description=test_description,count=test_number_of_questions,full_mark=test_full_mark),
                         reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Testni boshlash",callback_data="start_test-"+test_id)),parse_mode="HTML")
    except Exception as e:
        logging.error(e,stack_info=True)
def test_step(msg:Message,test_id: str):
    try:
        # test_id = msg.text.split("-")[0]
        # print(msg.chat.id)
        test_model = TestModel.objects.get(id=test_id)
        if OngoingTests.objects.filter(user=User.get(uid=msg.chat.id)).first() is not None:
            bot.send_message(msg.chat.id,Texts.have_already_started, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Testga o'tish",callback_data="restart_test-"+test_id)))
            return
        test = Test(bot,msg.chat.id,test_id)
        # Completely useless
        new_test = OngoingTests.objects.create(quiz=test_model,user=User.get(uid=msg.chat.id))
        new_test.user_answers=test.testData.answers
        new_test.save()
        # Ending useless part
        test.start()
        ongoing_tests[msg.chat.id] = test
    except Exception as e:
        logging.error(e,stack_info=True)


def del_msg(msg: Message):
    bot.delete_message(msg.chat.id, msg.id)


def check_test(callback: CallbackQuery):
    """
    Handle the callback query for the test.

    Args:
        callback (CallbackQuery): The callback query object.

    Returns:
        None
    """
    try:
        # Check if the callback is for starting a new test
        if callback.data.startswith("start_test-"):
            test_id = callback.data.split("-")[1]
            del_msg(callback.message)  # Delete the previous message
            test_step(callback.message, test_id)  # Start the test

        # Check if the callback is for restarting an existing test
        elif callback.data.startswith("restart_test-"):
            test_id = callback.data.split("-")[1]
            del_msg(callback.message)  # Delete the previous message

            # Check if the test is already ongoing
            if ongoing_tests.get(callback.message.chat.id) is None:
                # Create a new test instance
                ongoing_tests[callback.message.chat.id] = Test(
                    bot,
                    callback.message.chat.id,
                    test_id,
                    OngoingTests.objects.get(
                        user=User.objects.get(uid=callback.message.chat.id)
                    ).user_answers
                )

            test = ongoing_tests[callback.message.chat.id]
            test.restart()  # Restart the test

        # Check if the callback is for checking the test status
        else:
            if ongoing_tests.get(callback.message.chat.id) is None:
                # Create a new test instance if not already ongoing
                ongoing_tests[callback.message.chat.id] = Test(
                    bot,
                    callback.message.chat.id,
                    OngoingTests.objects.get(
                        user=User.objects.get(uid=callback.message.chat.id)
                    ).quiz.id,
                    OngoingTests.objects.get(
                        user=User.objects.get(uid=callback.message.chat.id)
                    ).user_answers,
                )

            is_finished = ongoing_tests[callback.message.chat.id].check_test(callback)
            if is_finished:
                del ongoing_tests[callback.message.chat.id]  # Remove the test from the ongoing list
                OngoingTests.objects.filter(
                    user=User.objects.get(uid=callback.message.chat.id)
                ).delete()  # Delete the test from the database

    except Exception as e:
        logging.error(e)
