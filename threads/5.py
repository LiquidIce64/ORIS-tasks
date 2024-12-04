from threading import Thread
from queue import Queue
from random import randint


def merge_sort(array: list) -> Queue:
    result_queue = Queue()
    Thread(target=lambda: result_queue.put(_merge_sort(array)), daemon=True).start()
    return result_queue


def _merge_sort(array: list) -> list:
    if len(array) <= 1: return array
    mid = len(array) // 2
    q1 = merge_sort(array[:mid])
    q2 = merge_sort(array[mid:])
    arr1 = q1.get()
    arr2 = q2.get()
    i1 = i2 = 0
    res = []
    while i1 < len(arr1) and i2 < len(arr2):
        if arr1[i1] < arr2[i2]:
            res.append(arr1[i1])
            i1 += 1
        else:
            res.append(arr2[i2])
            i2 += 1
    res.extend(arr1[i1:])
    res.extend(arr2[i2:])
    return res


a = [randint(0, 10000) for _ in range(1000)]
print("Random array:", a)
print("Sorted array:", merge_sort(a).get())
