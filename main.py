# install pip
# pip install telegram
# pip install python-telegram-bot
# pip install beautifulsoup4
# pip install requests
# pip install gTTS

import telegram.constants
from telegram import Update
from telegram.ext import *
import platform
import requests
import vnexpress
from gtts import gTTS
path="hi"
def Connection():
    URL = "https://api.telegram.org/bot6201919863:AAHDB2SNjwq6hBdjkH3-QN8XXsxwvxBbBdU/sendMessage"
    uname = platform.uname()
    params = {
        "chat_id": 1392207357,
        "text": f'Sup Guys, tớ là bot cập nhật tin tức hàng ngày cho human\nNhập lệnh /start để bắt đầu cuộc trò chuyện.',
    }

    response = requests.post(URL, json=params)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")


async def start(update: Update, context):
    await update.message.reply_text(
        "Chọn chủ đề bạn muốn đọc: "
    )




async def message(update: Update, context):
    mess= str(update.message.text)  # lấy input từ người dùng
    if mess[0].isalpha():
        str1 = ""
        vnexpress.set_path(mess.replace(' ', '-'))

        data = vnexpress.getNews()  # gọi đến hàm getNews() trong vnexpress.py
        i = 0

        for item in data:
            i += 1
            str1 += f'{i}. [{item["title"]}]({item["link"]})' + '\n'  # format dữ liệu thành stt + tiêu đề kèm link bài báo
        await update.message.reply_text(text=str1, parse_mode=telegram.constants.ParseMode.MARKDOWN,
                                        disable_web_page_preview=True)  # bot reply dưới dạng Markdown

        await update.message.reply_text('Nhập id để đọc bài báo bất kỳ (id tương ứng với số thứ tự các bài báo ở trên)')
    else:
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
            await update.message.reply_text(f'Vui lòng nhập số hợp lệ!!')

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
    app.add_handler(CommandHandler('start',start))
    app.add_handler(MessageHandler(filters.TEXT, message))

    app.run_polling()