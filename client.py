from socket import *
from time import sleep
import base64

username = '554475362@qq.com'
auth_code = 'ihrcsysdpfgkbcji'
mail_server = 'smtp.qq.com'
port = 25
BUF_SIZE = 1024
default_title = "I love computer network!"
default_msg = "This a test email ^_^"
helo_command = "HELO Thor"
login_command = "auth login"
data_command = "data"
quit_command = "quit"
image_type = 'image/jpeg'
text_type = 'text/plain'
MIME_version = "MIME-Version:1.0"
tail = '\r\n'


def get_from():
    return 'mail from: <' + username + '> ' + tail


def get_to(to_address):
    return 'rcpt to: <' + to_address + '> ' + tail


def get_header(content_type):
    return '--lines' + tail + 'Content-Type:' + content_type + tail + tail


def get_footer():
    return tail + '.' + tail


class Email:
    def __init__(self, to_address):
        self.to_address = to_address
        self.username = base64.b64encode(username.encode('utf-8'))
        self.auth_code = base64.b64encode(auth_code.encode('utf-8'))
        # create socket
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((mail_server, port))
        recv = self.sock.recv(BUF_SIZE).decode('utf-8')
        print(recv)
        if recv[:3] != '220':
            print('220 reply not received from server.')

    def send_email(self, title=default_title, msg=default_msg, img=None):
        # send helo msg
        print("helo")
        self.send_msg(helo_command+tail, '250')
        # send login command
        print("login")
        self.send_msg(login_command+tail, '334')
        # send username and auth code to login
        print("auth")
        self.send_encode(self.username, '334')
        self.send_encode(self.auth_code, '235')
        # send email from and to command
        print("from to")
        self.send_msg(get_from(), '250')
        self.send_msg(get_to(self.to_address), '250')
        # send data command
        print("data")
        # send msg
        self.send_msg(data_command+tail, '354')
        print("msg")
        # send img
        self.sock.send(self.build_msg(title, msg).encode('utf-8'))
        if img:
            print("img")
            self.send_img(img)
        print("footer")
        self.send_msg(get_footer(), '250')
        # send quit
        print("quit")
        self.send_msg(quit_command + tail, '221')

    def build_msg(self, title, msg):
        from_msg = 'from: <' + username + '> ' + tail
        to_msg = 'to: <' + self.to_address + '> ' + tail
        header = from_msg + to_msg
        subject = "subject:" + title + tail
        content_type = 'Content-Type:multipart/mixed;boundary=lines' + tail + tail
        head = header + subject + MIME_version + tail + content_type
        msg_header = get_header(text_type)
        msg = msg + tail
        return head + msg_header + msg

    def send_msg(self, msg, status_code):
        self.sock.send(msg.encode('utf-8'))
        sleep(1)
        recv = self.sock.recv(BUF_SIZE).decode('utf-8')
        print(recv)
        if recv[:3] != status_code:
            print('%s reply not received from server.' % status_code)

    def send_img(self, img):
        header = '--lines' + tail + 'Content-Type:image/jpeg; name=%s' % img + tail +\
                 'Content-Transfer-Encoding: ' + 'base64' + tail + tail
        with open(img, 'rb') as f:
            image = base64.b64encode(f.read())
        footer = tail + '--lines--' + tail
        self.sock.send(header.encode('utf-8'))
        self.sock.send(image)
        self.sock.send(footer.encode('utf-8'))

    def send_encode(self, msg, status_code):
        self.sock.send(msg)
        self.sock.send(tail.encode('utf-8'))
        sleep(1)
        recv = self.sock.recv(BUF_SIZE).decode('utf-8')
        print(recv)
        if recv[:3] != status_code:
            print('%s reply not received from server.' % status_code)


if __name__ == '__main__':
    email = Email("821403039@qq.com")
    email.send_email(img='DSC_1460.jpg')
