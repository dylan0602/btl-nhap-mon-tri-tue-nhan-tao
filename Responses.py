import datetime as dtm
from unidecode import unidecode

topics = ["tin tuc 24h","the gioi","kinh doanh","khoa hoc","giai tri","the thao","phap luat","giao duc","suc khoe","doi song","du lich","so hoa","thu gian"]

type = ""
def sample_response(input):
    user_mess = str(input).lower()
    global type

    if user_mess in ("hi", "hello", "ok"):
        type = "greeting"
        return "Hi Bro :v"
    elif user_mess in ("time", "time?"):
        type = "greeting"
        now = "Hôm nay là: " + dtm.now().strftime("%d-%m-%y, %H:%M:%S")
        return str(now)
    elif user_mess.isnumeric():
        type='number'
        return user_mess
    else:
        for topic in topics:
            if unidecode(user_mess).lower().__contains__(topic):
                type="topic"
                return user_mess
        return "Không tìm thấy chủ đề!!!"



    return "Hmmm..."

def write_file(str):
    file = open("output.txt", "w", encoding="utf-8")
    file.write(str)
    file.close()

