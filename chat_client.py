'''
    客户端
'''
from socket import *
import os, sys

# 服务器地址
ADDR = ('176.209.104.27', 18833)


def send_msg(s, name):
    '''
        发消息
    :param s:
    :param name:
    :return:
    '''
    while True:
        try:
            text = input('发言:')
        except KeyboardInterrupt:
            text = 'quit'
        # 退出聊天室
        if text == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), ADDR)
            sys.exit('退出聊天室')
        msg = 'C %s %s' % (name, text)
        s.sendto(msg.encode(), ADDR)


def recv_msg(s):
    '''
        收消息
    :param s:
    :return:
    '''
    while True:
        data, addr = s.recvfrom(2048)
        # 服务端发送EXIT表示让客户端退出
        if data.decode == 'EXIT':
            sys.exit()
        print(data.decode()+'\n发言:',end='')


# 创建网络连接
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input('请输入姓名')
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = s.recvfrom(1024)
        if data.decode() == 'ok':
            print('你已经进入聊天室')
            break
        else:
            print(data.decode())
    # 创建新的进程
    pid = os.fork()  #
    if pid < 0:
        sys.exit('Error')
    elif pid == 0:
        send_msg(s, name)
    else:
        recv_msg(s)


if __name__ == '__main__':
    main()