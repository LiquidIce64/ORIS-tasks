import queue
import threading


def factorial(n: int, max_threads=16, min_per_thread=8):
    result = 1
    tasks = 0
    n_per_thread = max(min_per_thread, (n + max_threads - 2) // max_threads)
    output_queue = queue.Queue()

    def _factorial(_start, _end, _output_queue):
        res = 1
        for i in range(_start, _end + 1):
            res *= i
        _output_queue.put((_start, _end, res))

    while n > 1:
        tasks += 1
        start = n - n_per_thread
        threading.Thread(target=_factorial, args=(max(2, start + 1), n, output_queue)).start()
        n = start
    for _ in range(tasks):
        start, end, r = output_queue.get()
        print(f"{start}\tto {end}\tmultiplied = {r}")
        result *= r
    return result


inp = int(input("Input integer: "))
threads = int(input("Input max threads amount: "))
print(f"{inp}! = {factorial(inp, threads)}")
