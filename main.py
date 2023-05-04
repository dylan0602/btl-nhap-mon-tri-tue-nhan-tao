# install pip
# pip install telegram
# pip install python-telegram-bot
# pip install beautifulsoup4
# pip install requests
# pip install gTTS

import telegram.constants
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
import platform
import requests
import os
import vnexpress
from gtts import gTTS


SITE = range(1)

# Kết nối, sử dụng thư viện requests để post 1 request tới api của telegram bot, nếu kết nối thành công thì sẽ hàm status_code sẽ trả về giá trị 200
def Connection():
    URL = "https://api.telegram.org/bot6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU/sendMessage"
    uname = platform.uname()
    params = {
        "chat_id": 1392207357,
        "text": f'Sup Guys, tớ là bot cập nhật tin tức hàng ngày cho human\nNhập lệnh /start để bắt đầu cuộc trò chuyện, /stop để dừng cuộc trò chuyện này\n\n',
    }

    response = requests.post(URL, json=params)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")

# bắt đầu cuộc trò chuyện với việc tạo ra box để lựa chọn website tin tức
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation"""
    reply_keyboard = [["Vnexpress"]]

    await update.message.reply_text(
        "Chọn website tin tức mà bạn muốn đọc: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )

    return SITE

# Stop cuộc trò chuyện
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "Bye, hẹn gặp lại!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

'''
gửi nội dung chi tiết bài báo tương ứng với nội dung người dùng nhập vào là 1 id
sau đó gửi file audio convert từ string sử dụng gTTS, api cung cấp bới Google
'''
async def message(update: Update, context):
    message = str(update.message.text)  # lấy input từ người dùng
    str1 = ""
    data = vnexpress.getNews()  # gọi đến hàm getNews() trong vnexpress.py
    i = 0
    for item in data:
        i += 1
        str1 += f'{i}. [{item["title"]}]({item["link"]})' + '\n'  # format dữ liệu thành stt + tiêu đề kèm link bài báo
    await update.message.reply_text(text=str1, parse_mode=telegram.constants.ParseMode.MARKDOWN, disable_web_page_preview=True)  # bot reply dưới dạng Markdown

    await update.message.reply_text('Nhập id để đọc bài báo bất kỳ (id tương ứng với số thứ tự các bài báo ở trên)')

# hàm xử lý cho phép người dùng lựa chọn 1 bài báo bất kỳ để đọc, bot sẽ trả về output dưới dạng text của bài báo đó, kèm theo ngay sau đó là 1 bản audio được convert sang sử dụng api gTTS do google cung cấp
async def read_article(update: Update, context):
    try:
        choice = int(update.message.text)
        article = vnexpress.getNews()[choice - 1]['link']
        result = str(vnexpress.getContents(article))  # lấy nội dung bài báo từ hàm getContents()
        if len(result.split()) >= 500:  # Nếu nội dung bài báo dài hơn 500 từ => ghi vào 1 file và gửi lại cho người dùng (Do message mà bot gửi lên bị giới hạn kích thước)
            write_file(result)
            await update.message.reply_text('Dài quá. Đợi 1 lúc tớ sẽ chép vào 1 file nhé!')
            await update.message.reply_document("output.txt")
        else:
            await update.message.reply_text(text=result, parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                            disable_web_page_preview=True)
            audio(result)
    except(ValueError, IndexError):
        await update.message.reply_text(f'Vui lòng nhập số hợp lệ trong đoạn {1}-{len(vnexpress.getNews())}!!')


# Hàm convert từ string sang audio
def audio(text):
    tts = gTTS(text, lang='vi', slow=False)
    audio_file = f'audio.mp3'
    tts.save(audio_file)
    with open('audio.mp3', 'rb') as audio: # Gửi payload chứa thông tin chat_id của bot, title audio kèm với file audio
        payload = {
            'chat_id': 1392207357,
            'title': 'audio.mp3',
        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            "https://api.telegram.org/bot6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU/sendAudio".format(
                token='6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU'),
            data=payload,
            files=files).json()
    audio.close()

def write_file(str):
    file = open("output.txt", "w", encoding="utf-8")
    file.write(str)
    file.close()

if __name__ == "__main__":
    Connection()

    app = ApplicationBuilder().token("6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU").build()
    '''
    ConversationHandler: quản lý luồng trò chuyện
    CommandHandler: đưa vào 1 câu lênh (format: /command )
    MessageHandler: xử lý các tin nhắn gửi đến bot (dưới dạng văn bản)
    '''
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SITE: [MessageHandler(filters.Regex("^(Vnexpress)$"), message)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT, read_article))

    app.run_polling()