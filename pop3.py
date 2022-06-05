import ssl
import socket
import time
from urllib.request import urlopen


def pop3handler(number, command, numberOflines='0'):
    if not connect():
        return
    def request(socket, request):
        socket.send((request + '\n').encode())
        recv_data = socket.recv(65535).decode()

        return recv_data

    def get_headers(number, lines='0'):
        summ = b''
        request(client, f"TOP {number} {lines}")
        while True:
            cur = request(client, f"TOP {number} {lines}")
            time.sleep(0.5)

            summ += cur.encode('utf-8')
            if '+OK ' in cur:
                break
        return summ

    def get_full_message(number):
        summarize = b''
        request(client, f"RETR {number}")
        while True:
            cur = request(client, f"RETR {number}")
            time.sleep(0.5)

            summarize += cur.encode('utf-8')
            if '+OK' in cur:
                break
        return summarize

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('pop3.yandex.ru', 995))
        client = ssl.wrap_socket(client)
        ready = client.recv(1024).decode()
        if '+OK' in ready:
            print('Сервер готов.')
        else:
            print('Сервер не готов.')
            return
        login = ''
        password = ''
        login_init = request(client, "USER " + login)
        if '+OK' in login_init:
            print('Введите пароль.')
        else:
            print('Возникла непредвиденная ситуация при авторизации. ')
        req = request(client, "PASS " + password)
        if '-ERR' in req:
            print('Неправильная комбинация логин-пароль,повторите снова.')
            return
        else:
            print('Вход выполнен.')
        if command == 'TOP':
            b = get_headers(number, numberOflines)
        else:
            b = get_full_message(number)

        with open('result.txt', 'wb') as f:
            f.write(b)
        print('Результат выполнения находится в result.txt текущей директории.')
        return


def connect():
    try:
        urlopen('http://google.com')
        return True
    except:
        print("нет соединения")
        return False


if __name__ == '__main__':
    message=input('Введите номер необходимого сообщения. 1-номер самого свежего сообщения :')
    method = input(
        'Введите метод.RETR - для получения содержимого сообщения,TOP - для получения заголовков :')
    linesCount=input(
        'Если Вы выбрали метод TOP и необходимо получить часть сообщения,введите количество необходимых строк :')
    pop3handler(message,method,linesCount)


