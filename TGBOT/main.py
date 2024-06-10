import time

from telebot import TeleBot
from telebot.types import Message, CallbackQuery
from buttons import gentest_markup, genlist_markup, remove_markup
from Tester import Test
bot = TeleBot(token="6129241988:AAGSeBfqRlEM5-eQUDXpNwOhcMfojkeLDHs")
# bot.delete_webhook()
@bot.message_handler(commands=["start"])
def send_hello(msg: Message):
    bot.send_message(msg.chat.id,
                     f"Assalomu alaykum {msg.chat.first_name}\nBotdan foydalanish uchun ro'yxatdan o'ting!")


@bot.message_handler(commands=['tests'])
def tests_function(msg: Message):
    try:
        mark = genlist_markup(['0001-Python', '0002- Fizika'])
        bot.reply_to(msg, "📄Quyidagi testlardan birini tanlang👇", reply_markup=mark)
        bot.register_next_step_handler(msg, test_step)
    except Exception as e:
        print("ERROR(tests_function): ", e)
ongoing_tests = dict()

def test_step(msg: Message):
    try:
        id = msg.text.split('-')[0]
        test = Test(bot,msg.chat.id,id)
        test.start()
        ongoing_tests[msg.chat.id] = test

    except Exception as e:
        print("ERROR(test_step): ", e)





def del_msg(msg: Message):
    bot.delete_message(msg.chat.id, msg.id)


@bot.callback_query_handler(func=lambda callback: True)
def check_test(callback: CallbackQuery):
    try:
        ongoing_tests[callback.message.chat.id].check_test(callback)
    except Exception as e:
        print("ERROR(check_test): ", e)


if __name__ == "__main__":
    bot.infinity_polling()
