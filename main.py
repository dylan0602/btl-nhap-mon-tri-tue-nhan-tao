import requests

import Constants as keys
import Responses as R
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, Updater
import vnexpress
import datetime as dtm
from datetime import time
import pytz

bot=telegram.Bot(token=keys.API_KEY)
# Hàm khởi động với lệnh /start trong telegram
def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

    # update.message.reply_text(
    #     "Tin tức mởi nhất hôm nay\n"
    # )
    #
    # update.message.reply_text(tin_tuc_24h())
    update.message.reply_text(
        "Chọn chủ đề tin tức bạn muốn đọc: "
    )

def tin_tuc_24h(limit):
    str1 = ""
    vnexpress.set_path('tin-tuc-24h')

    data = vnexpress.getNews(limit)
    i = 0

    for item in data:
        i += 1
        str1 += f'{i}. [{item["title"]}]({item["link"]})' + '\n'  # format dữ liệu thành stt + tiêu đề kèm link bài báo
    return str1

# Hàm khởi động với lệnh /help trong telegram
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Bạn muốn tôi giúp gì?")

# Hàm khởi động với các câu hỏi trong file Response.py
def handle_message(update: Update, context: CallbackContext):
    text = str(update.message.text).lower()
    response = R.sample_response(text)

    if (isinstance(response, str)):
        update.message.reply_text(response, telegram.constants.PARSEMODE_MARKDOWN,disable_web_page_preview=True)
    else:
        file = open('output.txt',encoding="utf8")
        update.message.reply_document(file)

def auto_update(_):
    url = f'https://api.telegram.org/bot6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU/sendMessage?chat_id=1392207357&text='

    requests.get("Tin tức mới nhất hôm nay\n"+url+str(pytz.timezone('Asia/Ho_Chi_Minh').localize(dtm.datetime.now())))
    requests.get(url+tin_tuc_24h(5))
def main():
    updater = Updater(keys.API_KEY)
    dp = updater.dispatcher
    zone = pytz.timezone('Asia/Ho_Chi_Minh')

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler("help", help_command))
    updater.job_queue.run_daily(auto_update, time=time(7,0,0,tzinfo=zone)) # auto gửi tin tức mới nhất, cập nhật vào 7h sáng hàng ngày
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()


main()
