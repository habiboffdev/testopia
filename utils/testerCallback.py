from telebot import types

def gentest_markup(test):
    try:
        quiz = test.data[test.current_question]
        data = quiz
        check = test.answers[test.current_question]
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttons = []
        for index,key in enumerate(data['keys']):
            var = key
            if index == check and check!=-1:
                var = "✅ "+key
            button = types.InlineKeyboardButton(var, callback_data=str(index))
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
        print("ERROR(gentest_markup): ", e)

def genlist_markup(tests):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True )
        buttons = []
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