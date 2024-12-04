import threading
import time

num_threads = 0
result = 1


def factorial(n: int, split_size=8, max_threads=16, _start=2) -> int:
    global num_threads
    global result
    num_threads += 1
    split_point = _start + split_size
    if split_point < n:
        while num_threads > max_threads + 1:
            time.sleep(0.01)
        threading.Thread(target=factorial, args=(n, split_size, max_threads, split_point)).start()
        n = split_point - 1

    for i in range(_start, n + 1):
        result *= i

    num_threads -= 1


inp = int(input("Input integer: "))
factorial(inp)
while num_threads > 0:
    time.sleep(0.01)
print(f"{inp}! = {result}")
