from telebot import types
from .testModel import QuizUtil
from data.models import Choice
def gentest_markup(test:QuizUtil):
    try:
        data = test
        check = test.answers.choices
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttons = []
        for index,key in enumerate(Choice.objects.filter(question=data.current_question)):
            # print(buttons)
            var = key.text
            if check.filter(choice=key).exists():
                var = "✅ "+key.text
            button = types.InlineKeyboardButton(var, callback_data=str(key.id))
            buttons.append(button)
        if check!=-1:
            skip = types.InlineKeyboardButton('Keyingi',callback_data=f'next{check}',)
        else:
            skip = types.InlineKeyboardButton('O\'tkazib yuborish',callback_data='skip',)
        back = types.InlineKeyboardButton('Orqaga',callback_data='back')
        finish = types.InlineKeyboardButton('Tugatish',callback_data='finish')
        markup.add(*buttons)
        markup.row_width = 2
        markup.add(back,skip)
        markup.row_width = 1
        markup.add(finish)
        return markup
    except Exception as e:
        print("ERROR(gentest_markup): ", e.with_traceback(e.__traceback__))

def genlist_markup(tests):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True )
        for test in tests:
            markup.add(types.KeyboardButton(test+"📄"))
        return markup
    except Exception as e:
        print("Error(genlist_markup):",e)
def remove_markup():
    try:
        markup = types.ReplyKeyboardRemove()
        return markup
    except Exception as e:
        print("Error(genlist_markup):",e)