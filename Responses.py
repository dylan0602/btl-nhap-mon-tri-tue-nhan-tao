
import datetime as dtm
import Constants as keys
import requests
from gtts import gTTS
from unidecode import unidecode
import vnexpress
topics = ["tin tuc 24h","the gioi","kinh doanh","khoa hoc","giai tri","the thao","phap luat","giao duc","suc khoe","doi song","du lich","so hoa","thu gian"]

type = ""
def sample_response(input):
    user_mess = str(input).lower()
    global type

    if user_mess in ("hi", "hello", "ok"):
        type = "greeting"
        return "Hi Bro :v"
    if user_mess in ("time", "time?"):
        type = "greeting"
        now = "Hôm nay là: " + dtm.now().strftime("%d-%m-%y, %H:%M:%S")
        return str(now)
    for topic in topics:
        if unidecode(user_mess).lower().__contains__(topic):
            type="topic"
            return user_mess
    if user_mess[0].isdigit():
        try:
            choice = int(user_mess)
            article = vnexpress.getNews()[choice - 1]['link']
            result = str(vnexpress.getContents(article))  # lấy nội dung bài báo từ hàm getContents()
            if len(result.split()) >= 500:  # Nếu nội dung bài báo dài hơn 500 từ => ghi vào 1 file và gửi lại cho người dùng (Do message mà bot gửi lên bị giới hạn kích thước)
                write_file(result)

                try:
                    type = "file"
                    # audio(result)
                    return open('output.txt', encoding="utf8")
                except:
                    print('Error. Try again')
            else:
                type="content"
                # audio(result)
                return result
        except(ValueError, IndexError):
            return 'Vui lòng nhập số hợp lệ!!'

    return "Hmmm..."

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

