
import datetime as dtm
import Constants as keys
import requests
from gtts import gTTS
from unidecode import unidecode
import vnexpress
topic = ["tin tuc 24h","the gioi","kinh doanh","khoa hoc","giai tri","the thao","phap luat","giao duc","suc khoe","doi song","du lich","so hoa","thu gian"]
def sample_response(input):
    user_mess = str(input).lower()

    if user_mess in ("hi", "hello", "ok"):
        return "Hi Bro :v"
    if user_mess in ("time", "time?"):
        now = "Hôm nay là: " + dtm.now().strftime("%d-%m-%y, %H:%M:%S")
        return str(now)
    if unidecode(user_mess).lower() in topic and isinstance(user_mess, str):
        str1 = ""
        vnexpress.set_path(user_mess.replace(' ', '-'))

        data = vnexpress.getNews()
        i = 0

        for item in data:
            i += 1
            str1 += f'{i}. [{item["title"]}]({item["link"]})' + '\n'  # format dữ liệu thành stt + tiêu đề kèm link bài báo
        noti = "\nChọn bài báo để đọc (Nhập id bài báo tương ứng với stt ở trên):"
        return str1+noti

    else:
        if user_mess[0].isdigit():
            try:
                choice = int(user_mess)
                article = vnexpress.getNews()[choice - 1]['link']
                result = str(vnexpress.getContents(article))  # lấy nội dung bài báo từ hàm getContents()
                if len(result.split()) >= 500:  # Nếu nội dung bài báo dài hơn 500 từ => ghi vào 1 file và gửi lại cho người dùng (Do message mà bot gửi lên bị giới hạn kích thước)
                    write_file(result)
                    try:
                        audio(result)
                        return open('output.txt', encoding="utf8")
                    except:
                        print('Error. Try again')
                else:
                    audio(result)
                    return result
            except(ValueError, IndexError):
                return 'Vui lòng nhập số hợp lệ!!'
        else: return "Vui lòng chọn chủ đề phù hợp (Thế giới, Kinh doanh, Khoa học, Giải trí, Thể thao, Pháp luật, Giáo dục, Sức khỏe, etc.)"

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

