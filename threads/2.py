import math
import threading
import time

num_threads = 0


def get_primes(start, end, split_size=1000, max_threads=16):
    global num_threads
    num_threads += 1
    split_point = start + split_size
    if split_point < end:
        while num_threads > max_threads + 1:
            time.sleep(0.01)
        threading.Thread(target=get_primes, args=(split_point, end, split_size, max_threads)).start()
        end = split_point

    for i in range(start, end):
        for j in range(2, math.ceil(math.sqrt(i))):
            if i % j == 0: break
        else:
            print(i)

    num_threads -= 1


get_primes(100, 100000)
