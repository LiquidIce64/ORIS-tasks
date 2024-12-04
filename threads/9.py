from threading import Thread
from queue import Queue


SPLIT_SIZE = 4
POWER_LIMIT = 15000


def power(n: int, p: int, ret_queue: Queue, ret_is_print=False):
    other_half = None
    _p = p
    if p > SPLIT_SIZE:
        other_half = Queue()
        Thread(target=power, args=(n, p // 2, other_half), daemon=True).start()
        p -= p // 2

    try:
        res = 1
        for i in range(p):
            res *= n
        if other_half is not None:
            res *= other_half.get()
        ret_queue.put(f"{n} ^ {_p} = {res}" if ret_is_print else res)
    except Exception:
        ret_queue.put(f"An error occurred during calculation of {n} ^ {_p}")


def input_async(q: Queue):
    while True:
        inp = input()
        q.put(inp)
        if inp == "exit": break


def print_async(q: Queue):
    while True:
        print(q.get())


print("Input 2 integers with a space inbetween to calculate one raised to the power of another")
print("Type exit to stop the program")
input_queue = Queue()
Thread(target=input_async, args=(input_queue,), daemon=True).start()
print_queue = Queue()
Thread(target=print_async, args=(print_queue,), daemon=True).start()
while True:
    inp = input_queue.get()
    if inp == "exit": break
    try:
        n, p = map(int, inp.split())
        if p > POWER_LIMIT:
            print_queue.put(f"Error: exponent too big ({n} ^ {p})")
            continue
        print_queue.put(f"Calculating {n} ^ {p}...")
        Thread(target=power, args=(n, p, print_queue, True), daemon=True).start()
    except ValueError:
        print_queue.put(f"Error: invalid input ({inp})")
