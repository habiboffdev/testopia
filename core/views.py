"""
Main views file.
We'll be implementing the base control units here.

"""
# --- START: IMPORTS
# built-in
import logging
import traceback
from datetime import timedelta

# other/external
import telebot
# django-specific
from django.core.exceptions import ValidationError
from django.db.models import F, Q, Count, Exists
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# local
from core import models
from core.bot_version import bot
from subprocess import Popen, PIPE
# from core.models import User, Tip
# from greed_island.factory import bot as gi_bot, strings

# from greed_island.models import Tag

bot.set_webhook(url=settings.NGROK_URL+settings.BOT_TOKEN,)
print(settings.NGROK_URL+settings.BOT_TOKEN)
@csrf_exempt
def handle_webhook_requests(request):
    def setup(_bot: telebot.TeleBot, _request_id: str) -> None:
        # i decided to disable threading in order to preserve synchronous order
        _bot.threaded = True

        # i'm using dict as a context to share data between bot instances
        if hasattr(bot, 'context'):
            _bot.context[_request_id] = {'violation': False}
        else:
            _bot.context = {_request_id: {'violation': False}}

    def process_update(_bot: telebot.TeleBot, _update: telebot.types.Update):
        try:
            # process update with bot instance
            _bot.process_new_updates([_update])
        except telebot.apihelper.ApiTelegramException:
            logging.error(traceback.format_exc())

    if request.headers.get('content-type') == 'application/json':

        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        try:
            request_id = bot.generate_unique_id(json_string=json_string)
            # set-up initial configs/data
            setup(bot, request_id)

            try:
                process_update(bot, update)
                # for now, i'm using this hard coded flow of processing.
                # maybe i'll think of a controller interface later... maybe not.

                # anyway, we've just run first instance, and we got our results (in context).
                # we continue according to user behaviour: we do not run next bot in case of violation
            finally:
                # time to clean
                # remove redundant data from context. we've already used it and we don't need it anymore
                bot.context.pop(request_id)

        except KeyError:
            # we could not generate request id, because some keys were missing.
            # we just go with main instance in this case
            process_update(bot, update)

        return JsonResponse(dict(ok=True))
    else:
        return JsonResponse(dict(ok=False), status=400)