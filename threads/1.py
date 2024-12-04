import threading
import time


def f():
    time.sleep(1)


n = int(input("Enter number of threads: "))
for i in range(n):
    thread = threading.Thread(target=f)
    thread.start()
    print(f"Thread {i}: {thread.name}")
