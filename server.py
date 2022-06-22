# -*- coding=utf-8 -*-
import socket
import threading
import queue
from HttpHead import HttpRequest


# 每个任务线程
class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super().__init__()
        self.work_queue = work_queue
        # 修改daemon默认值，使主线程结束时直接退出
        self.daemon = True

    def run(self):
        while True:
            func, args = self.work_queue.get()
            func(*args)
            self.work_queue.task_done()


# 线程池
class ThreadPoolManger():
    def __init__(self, thread_number):
        self.thread_number = thread_number
        # 创建queue容器
        self.work_queue = queue.Queue()
        for i in range(self.thread_number):    
            thread = WorkThread(self.work_queue)
            thread.start()

    def add_work(self, func, *args):
        self.work_queue.put((func, args))

# tcp连接设置
def tcp_link(sock, addr):
    print('Accepting a connection from %s:%s' % addr)
    request = sock.recv(1024)
    http_req = HttpRequest()
    http_req.passRequest(request)
    sock.send(http_req.getResponse().encode('utf-8'))
    sock.close()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 在9999端口上监听
    s.bind(('127.0.0.1', 9999))
    s.listen(10)
    thread_pool = ThreadPoolManger(5)
    print('listening on %s:%d' % ('127.0.0.1', 9999))
    while True:
        sock, addr = s.accept()
        thread_pool.add_work(tcp_link, *(sock, addr))

if __name__ == '__main__':
    start_server()

