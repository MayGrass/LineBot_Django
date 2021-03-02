from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.body.decode("utf-8")

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            print(
                print("Invalid signature. Please check your channel access token/channel secret.")
            )
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        else:
            return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
