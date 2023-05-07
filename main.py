import requests
from gtts import gTTS

import Constants as keys
import Responses
import Responses as R
import telegram
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, Filters, Updater
import vnexpress
import datetime as dtm
from datetime import time
import pytz
from unidecode import unidecode
import time as timee

topics = ["tin tuc 24h","the gioi","kinh doanh","khoa hoc","giai tri","the thao","phap luat","giao duc","suc khoe","doi song","du lich","so hoa","thu gian"]

bot=telegram.Bot(token=keys.API_KEY)
# Hàm khởi động với lệnh /start trong telegram
def start_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')
    update.message.reply_text(
        "Bạn muốn đọc tin tức về chủ đề gì? "
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
    update.message.reply_text("""
Nhập lệnh /start để bắt đầu cuộc trò chuyện
Tôi sẽ giúp bạn lấy những đầu báo đi kèm với link, đa dạng chủ đề mà bạn muốn
Bạn có thể đọc chi tiết một bài báo cụ thể. Nếu bài báo quá dài, thì tôi sẽ gửi 1 file chứa nội dung trong đó
Ngoài ra, tôi có thể gửi thêm 1 file audio tương ứng cho bài báo đó.
Các tin tức mới nhất sẽ được liên tục cập nhật vào 7:00 sáng mỗi ngày, và tôi sẽ làm điều đó cho bạn
    """)

# Hàm khởi động với các câu hỏi trong file Response.py
def handle_message(update: Update, context: CallbackContext):
    text = str(update.message.text).lower()
    response = R.sample_response(text)

    check = False
    i = 0
    if(Responses.type=="topic"):
        for topic in topics:
            if unidecode(response).lower().__contains__(topic):
                check = True
                vnexpress.set_path(topic.replace(' ', '-'))

                data = vnexpress.getNews()
                i = 0
                index = unidecode(response).lower().find(topic)
                update.message.reply_text("Đợi 1 chút! Tôi sẽ lấy bài báo liên quan đến chủ đề "+response[index:index+len(topic)].upper())
                timee.sleep(2)
                for item in data:
                    i += 1
                    update.message.reply_text(f'{i}. {item["title"]}\n{item["link"]}')
                update.message.reply_text("Nhập id tương ứng với stt các bài báo trên để đọc chi tiết")
        if check==False:
            update.message.reply_text("Không tìm thấy chủ đề!!!")
    elif(response.isnumeric()):
        try:
            choice = response
            article = vnexpress.getNews()[int(choice) - 1]['link']
            result = str(vnexpress.getContents(article))  # lấy nội dung bài báo từ hàm getContents()
            if len(result.split()) >= 500:  # Nếu nội dung bài báo dài hơn 500 từ => ghi vào 1 file và gửi lại cho người dùng (Do message mà bot gửi lên bị giới hạn kích thước)
                write_file(result)

                try:
                    # audio(result)
                    update.message.reply_document(open('output.txt', encoding="utf8"))
                except:
                    print('Error. Try again')
            else:
                # audio(result)
                update.message.reply_text(result)
        except(ValueError, IndexError):
            update.message.reply_text(f'Vui lòng nhập id hợp lệ!!')
    elif(Responses.type=="greeting"):
        update.message.reply_text(response)

def write_file(str):
    file = open("output.txt", "w", encoding="utf-8")
    file.write(str)
    file.close()

def audio(text):
    text1 = text[0:len(text)//5]
    tts = gTTS(text1, lang='vi', slow=False)
    audio_file = f'output.mp3'
    tts.save(audio_file)
    with open('output.mp3', 'rb') as audio: # Gửi payload chứa thông tin chat_id của bot, title audio kèm với file audio
        payload = {
            'chat_id': keys.CHAT_ID,
            'title': 'output.mp3',
        }
        files = {
            'audio': audio.read(),
        }
        resp = requests.post(
            f"https://api.telegram.org/bot{keys.API_KEY}/sendAudio".format(
                token=keys.API_KEY),
            data=payload,
            files=files).json()
    audio.close()


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
