from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtGui
from dex_nov import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from ftplib import FTP
from PyQt5.QtGui import QPixmap
import time
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import shutil
import socket
import imaplib, email, os
from PIL import Image


def main():
    class mywindow(QtWidgets.QMainWindow):
        def __init__(self, parent=None):
            super(mywindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.pushButton.setText('Применить')
            self.ui.pushButton_2.setText('Скриншот')
            self.ui.pushButton_2.clicked.connect(self.screen_tacker)
            self.ui.pushButton_3.clicked.connect(self.ban_button)
            self.ui.pushButton.clicked.connect(self.use_filter)
            self.current_id = 0
            self.ftp_serv = FTP('', user='', passwd='', timeout=600)
            self.ui.label_2.setText('Статус')
            self.ui.label.setText('')
            self.ui.pushButton_4.setText("Обновить логи")
            self.ui.pushButton_4.clicked.connect(self.log_refresh)
            self.ui.textBrowser.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)

        def scale_image(self,
                        input_image_path,
                        output_image_path,
                        width=None,
                        height=None
                        ):
            original_image = Image.open(input_image_path)
            w, h = original_image.size
            print('The original image size is {wide} wide x {height} '
                  'high'.format(wide=w, height=h))

            if width and height:
                max_size = (width, height)
            elif width:
                max_size = (width, h)
            elif height:
                max_size = (w, height)
            else:
                # No width or height specified
                raise RuntimeError('Width or height required!')

            original_image.thumbnail(max_size, Image.ANTIALIAS)
            original_image.save(output_image_path)

            scaled_image = Image.open(output_image_path)
            width, height = scaled_image.size
            print('The scaled image size is {wide} wide x {height} '
                  'high'.format(wide=width, height=height))

        def load_txt(self):
            ftp = FTP('', user='', passwd='', timeout=600)
            lst = ftp.nlst()
            try:
                out = 'all_comp_log.txt'
                # print(lst[i], day_cat)
                with open(out, 'wb') as f:
                    ftp.retrbinary('RETR ' + f'all_comp_log.txt', f.write)
            except:
                pass

        def load_zaban(self):
            lst = ftp.nlst
            try:
                out = 'banned_list.txt'
                with open(out, 'wb') as f:
                    ftp.retrbinary('RETR ' + f'banned_list.txt', f.write)
            except:
                pass

        def looad_screenloader(self):
            ftp = FTP('', user='', passwd='', timeout=600)
            lst = ftp.nlst()
            try:
                out = 'screen_shot_taker_loader.txt'
                # print(lst[i], day_cat)
                with open(out, 'wb') as f:
                    ftp.retrbinary('RETR ' + f'screen_shot_tacer_loader.txt', f.write)
            except:
                pass

        def send_id_text(self):
            f = open('all_comp_log.txt', "r")
            scl = f.read()
            b_scl_strs = scl.split("\n")
            b_text_for_returning = []
            for i in b_scl_strs:
                if str(self.current_id) in i:
                    b_text_for_returning.append(i)
            return b_text_for_returning

        def scroll_obnov(self):
            print(1)
            self.ui.scrollArea.setWidgetResizable(True)
            self.scroll = self.ui.scrollArea  # Scroll Area which contains the widgets, set as the centralWidget
            self.widget = QtWidgets.QWidget()  # Widget that contains the collection of Vertical Box
            self.vbox = QtWidgets.QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
            f = open("all_comp_list.txt", "r")
            s = f.read()
            b_id_s = s.split("+")
            for i in range(len(b_id_s)):
                if str(b_id_s) != '':
                    object = QtWidgets.QPushButton(str(b_id_s[i]))
                    object.clicked.connect(partial(self.get_new_current_id, object))
                    self.vbox.addWidget(object)

            self.widget.setLayout(self.vbox)

            # Scroll Area Properties
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll.setWidgetResizable(True)
            self.scroll.setWidget(self.widget)

        def use_filter(self):
            print(self.ui.textBrowser.toPlainText())
            tx_to_find = self.ui.textBrowser.toPlainText()
            self.ui.label_2.setText("12")
            f = open(f"{self.current_id}.txt")
            b_tx = f.read().split("\n")
            for i in b_tx:
                if tx_to_find in i.split(" "):
                    pixmap = QPixmap("filt_chec_succsess.bmp")
                    self.ui.label_2.setPixmap(pixmap)
                    self.ui.label_2.show()
                    return True
            pixmap = QPixmap("filt_chec_fail.bmp")
            self.ui.label_2.setPixmap(pixmap)
            self.ui.label_2.show()
            return False

        def screen_tacker(self):
            self.parser_image()
            self.scale_image(f"{str(self.current_id)}.bmp", f"{self.current_id}.bmp", 471, 261)
            pix = QPixmap(f"{str(self.current_id)}.bmp")
            item = QtWidgets.QGraphicsPixmapItem(pix)
            scene = QtWidgets.QGraphicsScene(self)
            scene.addItem(item)
            self.ui.graphicsView.setScene(scene)

        def ban_button(self):
            if not self.is_user_banned():
                f = open("banned.txt", "a")
                f.write(f"*{str(self.current_id)}")
                self.log_refresh()
                f.close()

        def unban(self):
            f = open("banned.txt", "r")
            str_to_unban = f.read()
            new_str = ""
            b_zabenen = str_to_unban.split("*")
            for i in str_to_unban:
                if i != str(self.current_id):
                    new_str += "*" + str(i)
            f.close()
            f = open("banned.txt", "w")
            f.write(new_str)
            f.close()
            self.ui.pushButton_3.setText("BAN")
            self.ui.pushButton_3.clicked.connect(self.ban_button)
            self.log_refresh()

        def is_user_banned(self):
            f = open("banned.txt", "r")
            ms_zaban = str(f.read()).split("*")
            f.close()
            if self.current_id in ms_zaban:
                return True
            return False

        def get_new_current_id(self, obj):
            shost = obj.text()
            self.current_id = shost
            self.log_refresh()
            print(shost)

        def log_refresh(self):
            print("entered func", self.current_id)
            self.email_logwriter()
            print(self.current_id)
            f = open(f"{self.current_id}.txt", "r")
            text = f.read()
            print(text)
            self.ui.label.setText(text)
            f.close()
            self.scroll_obnov()
            print("passed logwriter")
            if self.is_user_banned():
                self.ui.pushButton_3.setText("UNBAN")
                self.ui.pushButton_3.show()
                self.ui.pushButton_3.clicked.connect(self.unban)
                self.ui.label.setText('BANNED')
            """
            else:
                tex = self.send_id_text()
                s = ""
                for i in tex:
                    s += i + '\n'
                self.ui.label.setText(s)
            print("passed check for ban")
            print("passed creation of lables")
            f = open('all_comp_list.txt', 'w+')
            b_ind = str(f.read()).split("+")
            for i in range(len(b_ind)):
                if i == 0:
                    otv = b_ind[i][2:]
                elif i == len(b_ind) - 1:
                    otv = b_ind[i][:-1]
                else:
                    otv = b_ind[i]
            print("function sucsessfuly ended")
    """
        def add_id_to_list(self, id):
            f = open("all_comp_list.txt", "a")
            f.write(f"+{str(id)}")
            f.close()

        def ftp_upload(self, path, ftype='TXT'):
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

        def email_parser(self):
            user = "zay1bob@gmail.com"
            password = "JojobizzareAdventures"
            imap_url = "imap.gmail.com"
            retx = ""
            connection = imaplib.IMAP4_SSL(imap_url)
            connection.login(user, password)
            connection.select()
            result, data = connection.uid('search', None, "ALL")
            if result == 'OK':
                print("OK")
                result, data = connection.uid('fetch', data[0].split()[-1], '(RFC822)')
                if result == 'OK':
                    print("OK")
                    email_message = email.message_from_bytes(data[0][1])
                    content_of_email = email_message.get_payload()[1]
                    connection.close()
                    connection.logout()
                    retx = content_of_email
            print(retx.get_payload())
            if retx.get_content_type() == 'text/plain':
                st_chk = retx.get_payload()
                b_chk = st_chk.split(" ")
                f = open("all_comp_list.txt", "r")
                if b_chk[0] not in f.read().split("+"):
                    self.add_id_to_list(b_chk[0])
                f.close()
                print(1)
                print(retx)
                return retx.get_payload()

        def email_logwriter(self):
            str_of_log = self.email_parser()
            ms_str_of_log = str_of_log.split(" ")
            str_check_insert = str(str_of_log[1] + ms_str_of_log[2])
            print(str_check_insert)
            print(ms_str_of_log[0])
            try:
                f = open(f"{str(ms_str_of_log[0])}.txt", "r")
                str_to_check_in = f.read().split("\n")
                print(str_to_check_in[-1])
                f.close()
                if str_check_insert[1:] not in str_to_check_in[-1]:
                    f = open(f"{str(ms_str_of_log[0])}.txt", "a")
                    print("opended file")
                    f.write(f"\n{str_of_log}")
                    f.close()
            except:
                f = open(f"{str(ms_str_of_log[0])}.txt", "w+")
                str_to_check_in = f.read().split("\n")
                print(str_to_check_in[-1])
                f.close()
                if str_check_insert[1:] not in str_to_check_in[-1]:
                    f = open(f"{str(ms_str_of_log[0])}.txt", "a")
                    print("opended file")
                    f.write(f"\n{str_of_log}")
                    f.close()


        def parser_image(self):
            username = "lisickinoezise@gmail.com"
            password = "Lis12ezik"
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(username, password)
            status, messages = imap.select("INBOX")
            N = 1

            messages = int(messages[0])
            print(messages)
            for i in range(messages, messages - N, -1):
                # fetch the email message by ID
                res, msg = imap.fetch(str(i), "(RFC822)")
                print(res)
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        print("Subject:", subject)
                        print("From:", From)
                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # print text/plain emails and skip attachments
                                    print(body)
                                elif "attachment" in content_disposition:
                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        folder_name = subject
                                        if not os.path.isdir(folder_name):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode()
                            if content_type == "text/plain":
                                # print only text email parts
                                print(body)
                        if content_type == "text/html":
                            # if it's HTML, create a new HTML file and open it in browser
                            filename = f"{self.current_id}.bmp"
                            filepath = os.path.join(filename)
                            # write the file
                            open(filepath, "w").write(body)
                            # open in the default browser
                            webbrowser.open(filepath)
                        print("=" * 100)
            # close the connection and logout
            imap.close()
            imap.logout()


    def sending_percedure_sock():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.1.**", 12345))
        s.listen(10)
        c, addr = s.accept()
        print('{} connected.'.format(addr))
        f = open("image.jpg", "rb")
        datas = f.read(1024)
        while datas:
            c.send(datas)
            datas = f.read(1024)
        f.close()
        print("Done sending...")


    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()