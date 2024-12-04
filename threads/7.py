from threading import Thread
from queue import Queue
from re import findall


def _word_freq(text: list[str], return_queue: Queue):
    text = " ".join(text)
    result = {}
    word_count = 0
    words = findall(r"[a-zA-Zа-яА-Я]+", text)
    if words is not None:
        for word in words:
            word = word.lower()
            word_count += 1
            if word in result: result[word] += 1
            else: result[word] = 1
    return_queue.put((result, word_count))


def word_freq(text: list[str], max_threads=16):
    word_dict = {}
    total_words = 0
    lines_per_thread = (len(text) + max_threads - 1) // max_threads
    return_queue = Queue()
    threads = 0
    for i in range(0, len(text), lines_per_thread):
        threads += 1
        Thread(
            target=_word_freq,
            args=(text[i: i + lines_per_thread], return_queue),
            daemon=True
        ).start()
    while threads:
        ret_freq, ret_count = return_queue.get()
        total_words += ret_count
        for word, word_count in ret_freq.items():
            if word in word_dict: word_dict[word] += word_count
            else: word_dict[word] = word_count
        threads -= 1
    return [(
        word,
        word_count,
        word_count / total_words
    ) for word, word_count in word_dict.items()]


text = open("text.txt", encoding="utf-8").readlines()
freq = word_freq(text)
freq.sort(key=lambda x: x[0])
freq.sort(key=lambda x: x[1], reverse=True)
for word, count, freq in freq:
    print(f"{word}: {count} ({freq * 100:.2f}%)")
