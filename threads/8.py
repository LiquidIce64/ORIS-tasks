from __future__ import annotations
from typing import Callable
import os
from threading import Thread
from queue import Queue


class Worker(Thread):
    def __init__(self,
                 task_queue: Queue,
                 return_queue: Queue,
                 predicate: Callable[[str], bool]):
        super().__init__()
        self.task_queue = task_queue
        self.return_queue = return_queue
        self.pred = predicate

    def run(self):
        while True:
            directory_path: str | None = self.task_queue.get()
            if directory_path is None: break
            for name in os.listdir(directory_path):
                path = os.path.join(directory_path, name)
                if os.path.isfile(path):
                    if self.pred(path): self.return_queue.put(path)
                else:
                    self.task_queue.put(path)
            self.task_queue.task_done()


def print_queue(q: Queue):
    while True:
        print(q.get())
        q.task_done()


def on_tasks_finished(task_queue: Queue, threads: int):
    with task_queue.all_tasks_done:
        task_queue.all_tasks_done.wait()
    for _ in range(threads):
        task_queue.put(None)


def search_files(starting_directory: str, predicate: Callable[[str], bool], threads=16):
    return_queue = Queue()
    task_queue = Queue()
    task_queue.put(starting_directory)
    Thread(target=on_tasks_finished, args=(task_queue, threads)).start()
    for _ in range(threads):
        Worker(task_queue, return_queue, predicate).start()
    return return_queue


return_queue = search_files(os.curdir, lambda path: path.endswith(".py") and "\\venv\\" not in path)
Thread(target=print_queue, args=(return_queue,), daemon=True).start()

input()
