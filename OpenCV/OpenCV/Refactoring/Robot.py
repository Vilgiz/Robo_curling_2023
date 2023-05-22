from asyncio.log import logger
from distutils.log import debug
import socket
from threading import Thread
import time

import random

class Robot(Thread):

    
    def __init__(self, timeout=5, print_debug = False) -> None:
        Thread.__init__(self)

        self.HOST = ""
        self.PORT = 48569
        self.perm_start = False
        self.perm_step = False
        self.perm_stop = False
        self.is_connected = False
        self.timeout = timeout
        self.debug = print_debug
        self.__print("RobotDataThread object created")

    def __connect(self):
        self.__print("Server started. Waiting for connect...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen()
        conn, addr = s.accept()
        conn.settimeout(5)
        self.__print(f"Client with IP {addr} was connected")
        self.conn = conn
        self.__start = lambda: self.conn.sendall(b'start;')

        # Генерируем первое случайное число
        num1 = random.randint(1, 10)

        # Генерируем второе случайное число
        num2 = random.randint(1, 10)

        self.__cast = lambda path: self.conn.sendall(
            f'cast;{path[0][0]};{path[0][1]};{path[1][0]};{path[1][1]};{path[2]};{num1};{num2}'.encode())    #path
            #f'cast;{path[0][0]};{path[0][1]};{path[1][0]};{path[1][1]};{path[2]}'.encode())    #path
        self.__wait = lambda: self.conn.sendall(b'wait;')
        self.is_connected = True

    def __print(self, msg):
        if self.debug: print(msg)

    def __del__(self):
        self.perm_stop = True

    def run(self):
        self.__thread()
        self.__print("RobotData thread started")


    def stop(self):
        self.perm_stop = True

    def send_start(self):
        self.perm_start = True

    def send_step(self, path):
        self.path = path
        self.perm_step = True

    def __thread(self):
        self.__connect()
        time.sleep(1)
        while not self.perm_stop:
            try:
                if self.perm_start:
                    self.__start()
                    self.perm_start = False
                    _ = self.conn.recv(1024)
                    continue
                if self.perm_step:
                    self.__cast(self.path)
                    self.perm_step = False
                    _ = self.conn.recv(1024)
                    continue
                self.__wait()
                _ = self.conn.recv(1024)
                time.sleep(1)
            except Exception as msg:
                try:
                    self.conn.close()
                    self.is_connected = False
                except Exception:
                    pass
                self.__print("Connection broken or timeout exceeded. Restarting server")
                self.__connect()
        self.conn.close()
        self.is_connected = False
        self.__print("RobotData thread stopped")


if __name__ == "__main__":
    rdt = Robot(print_debug = True)
    rdt.start()
    rdt.send_start()
    for i in range(1, 9):
        s = input("->")
        p = s.split(' ')
        print(p)
        if len(p) == 3:
            rdt.send_step(p[0:2], p[2])