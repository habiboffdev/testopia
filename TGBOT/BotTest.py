import logging

from telebot import TeleBot

from telebot.types import Message, CallbackQuery
from .buttons import gentest_markup, genlist_markup, remove_markup
from .TestDealer import QuizUtil
from core.models import User
from data.models import Question

from time import sleep


class Test:
    def __init__(self, bot: TeleBot, chat_id: int, test_number: int, user_answer = None):
        """
        Initialize a new Test instance.

        Args:
            bot (TeleBot): The TeleBot instance.
            chat_id (int): The chat ID.
            test_number (int): The test number.
        """
        # Initialize the TeleBot instance.
        self.bot = bot

        # Initialize the chat ID.
        self.chat_id = chat_id

        # Get the User instance associated with the chat ID.
        self.user = User.get(uid=chat_id)

        # Initialize the test number.
        self.test_number = test_number

        # Initialize the QuizUtil instance for the test.
        self.testData: QuizUtil = QuizUtil(test_number, self.user,user_answer=user_answer)

        # Get the first question for the test.
        self.question: Question = self.testData.get_question()

        # Generate the markup for the test.
        self.markup = gentest_markup(self.testData)
        # Store all sent messages
        self.messages = []
    def start(self):
        """
        Start the test by sending a message to the chat.

        This function sends a message to the chat with a countdown for 3 seconds.
        After the countdown, it sends the first question of the test.

        Raises:
            Exception: If an error occurs while sending the message.
        """
        try:
            # Send a message with a countdown to the chat
            self.bot.send_message(
                chat_id=self.chat_id,
                text="<i>⏰Test 3 sekundda boshlanadi...</i>",
                parse_mode='HTML'  # Use HTML to format the message
            )

            # Wait for 3 seconds
            sleep(3)

            # Send the first question of the test to the chat
            self.messages.append(self.bot.send_message(
                chat_id=self.chat_id,
                text=self.question.text,
                reply_markup=self.markup,  # Use the markup for the test
                parse_mode="HTML"  # Use HTML to format the message
            ))
        except Exception as e:
            # Log the error
            logging.error(e)
    def restart(self):
        """
        Restart the test by sending the question text to the chat.

        This function sends the question text to the chat using the bot's send_message method.
        If an exception occurs during the process, it is logged.

        Raises:
            Exception: If an error occurs while sending the message.
        """
        try:
            for message in self.messages:
                try:
                    self.bot.delete_message(chat_id=self.chat_id, message_id=message.message_id)
                except Exception as e:
                    continue
            # Send the question text to the chat
            self.bot.send_message(
                chat_id=self.chat_id,
                text=self.question.text,
                reply_markup=self.markup,
                parse_mode="HTML"
            )
        except Exception as e:
            # Log the error
            logging.error(e)
    """
    Edit the message in the chat with the new question and the test markup.

    Args:
        msg (Message): The message to be edited.
    """

    def new_test(self, msg: Message):
        """
        Edit the message in the chat with the new question and the test markup.

        This function edits the message in the chat with the new question and the test markup.
        The new question is obtained from the get_question method of the test.
        The test markup is obtained from the gentest_markup function.
        The message is edited using the edit_message_text method of the bot.

        Args:
            msg (Message): The message to be edited.

        Raises:
            Exception: If an error occurs while editing the message.
        """
        try:
            # Get the new question from the test
            self.question = self.testData.get_question()
            self.markup = gentest_markup(self.testData)
            # Edit the message with the new question and the test markup
            self.bot.edit_message_text(
                chat_id=msg.chat.id,
                message_id=msg.id,
                text=self.question.text,
                reply_markup=self.markup,
                parse_mode='HTML'
            )
        except Exception as e:
            # Log the error
            logging.error(e)

    # For using callback_handler
    def check_test(self, callback: CallbackQuery) -> int:
        """
        Check the callback data and handle the test accordingly.

        Args:
            callback (CallbackQuery): The callback query object.

        Returns:
            1 if the test is finished, 0 otherwise.

        Raises:
            Exception: If an error occurs while editing the message.
        """
        try:
            # Get the callback data and message
            resp = callback.data
            msg = callback.message
            quiz = self.testData

            # Handle different callback data
            if resp == "back":
                # Do nothing
                pass
            elif resp == "skip":
                # Move to the next question
                self.new_test(msg)
            elif resp.startswith("next"):
                # Move to the next question
                self.new_test(msg)
            elif resp.isdigit():
                # Tick the answer and update the message
                self.testData.tick_answer(int(resp))
                self.bot.edit_message_text(
                    quiz.current_question.text, msg.chat.id, msg.id,
                    reply_markup=gentest_markup(self.testData), parse_mode="HTML")
            elif resp == "finish":
                # Finish the test and send the result
                self.bot.delete_message(msg.chat.id, msg.id)
                result = self.testData.get_result()
                question_count = self.testData.number_of_questions
                self.bot.send_message(
                    msg.chat.id,
                    "Natija: {}/{}".format(result, question_count),
                    parse_mode="HTML"
                )
                return 1
            return 0
        except Exception as e:
            # Log the error
            logging.error(e,stack_info=True)
