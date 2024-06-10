

class Texts:
    def __init(self,lang = "uz"):
        self.lang = lang
    welcome = "Assalomu alaykum"
    register_call_back = "Ro'yxatdan o'tish"
    register = "Iltimos ro'yxatdan o'ting"
    register_step_username = "Iltimos usernameni kiriting"
    register_done = "Ro'yxatdan o'tdingiz"
    register_step_username_wrong = "Username xato kiritildi.\n<b>Usernameda faqat lotin alifbolsi xarflari va _ belgisi bolishi mumkin!</b>"
    register_fullname = "Ism va familyangizni kiriting."
    register_age = "Yoshingiz? "
    have_already_started = "Bir vaqtda bir necha test ishlab bo'lmaydi!!!"
    test_info = "Test haqida ma'lumotlar\n<i>Nomi: </i>{test_name}\n<i>Ma'lumot: </i>{description}\n<i>Savollar soni: </i>{count}\n<i>Umumiy ball: </i>{full_mark}"
class Constants:
    STEP_USERNAME = 1
    STEP_FULLNAME = 2
    STEP_AGE = 3
