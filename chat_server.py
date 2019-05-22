'''
    Chat room
    env:python3.5
    socket fock 练习
'''
from socket import *
import os, sys

# 服务器地址
ADDR = ('0.0.0.0', 18833)
# 存储用户信息
user = {}


def do_login(s, name, addr):
    '''
        进入聊天室
    :param s:
    :param name:
    :param addr:
    :return:
    '''
    if name in user or '管理员' in name:
        s.sendto('该用户已存在'.encode(), addr)
        return
    s.sendto(b'ok', addr)
    # 通知其他人
    msg = '\n欢迎%s进入聊天室' % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    # 将用户加入
    user[name] = addr


def do_chat(s, name, text):
    '''
        发送xxx进入聊天室的消息给其他用户
    :param s:
    :param name:
    :param text:
    :return:
    '''
    msg = '%s:%s' % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


def do_quit(s, name):
    '''
        退出聊天室
    :param s:
    :param name:
    :return:
    '''
    msg = '%s退出聊天室' % name
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])
        else:
            s.sendto(b'EXIT', user[i])
    del user[name]


def do_request(s):
    '''
        处理请求
    :param s:
    :return:
    '''
    while True:
        data, addr = s.recvfrom(1024)
        msg = data.decode().split(' ')
        # 区分请求
        if msg[0] == 'L':
            do_login(s, msg[1], addr)
        elif msg[0] == 'C':
            text = ' '.join(msg[2:])
            do_chat(s, msg[1], text)
        elif msg[0] == 'Q':
            #当服务端退出,再重启,user清空
            if msg[1] not in user:
                s.sendto('EXIT', addr)
                continue
            do_quit(s, msg[1])


# 创建网络连接
def main():
    # 套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input('管理员有话说:')
            msg = 'C 管理员消息 ' + msg
            s.sendto(msg.encode(), ADDR)
    else:
        # 请求处理
        do_request(s)  # 处理客户端请求


if __name__ == '__main__':
    main()
