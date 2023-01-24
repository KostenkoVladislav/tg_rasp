import threading
import time


def sum(a, b):
    print(a + b)


t = threading.Timer(3, sum, args=(3,5))
t.start()
print('hello')
