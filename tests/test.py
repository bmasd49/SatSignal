import multiprocessing as mp 
from datetime import datetime
import numpy as np 
import os

class testdata:
    def __init__(self, data):
        self.data = data
    def increment(self, i):
        print("Testdata running")
        self.data[i] += 1

def task1(arg, queue):
    print(f"task 1 is running at {datetime.now().time()} with argument {arg} and processID {os.getpid()}")

    data = queue.get()
    print(f"Queue of task 1 is {data}")
    task3(data)
    print(f"Increasing first element by 1")
    
    data[0] += 1
    test = testdata(data)
    test.increment(2)
    queue.put(data)
    print(f"Queue of task 1 now is {data}\n\n")


def task2(arg, queue):
    print(f"task 2 is running at {datetime.now().time()} with argument {arg} and processID {os.getpid()}")
    data = queue.get()
    print(f"Queue of task 2 is {data}")
    task3(data)
    print(f"Increasing second element by 2")
    data[1] += 2
    test = testdata(data)
    test.increment(2)
    queue.put(data)
    print(f"Queue of task 2 now is {data}\n\n")
    test = testdata(data)
    test.increment(3)

def task3(data):
    print(f"This is task 3 with data {data} and now incresing 4th element by 4")
    data[3] += 4

if __name__ == "__main__":
    common = np.zeros(4)
    queue = mp.Queue()
    queue.put(common)
    p1 = mp.Process(target=task1, args=(common, queue))
    p2 = mp.Process(target=task2, args=(common, queue))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print("Done!")


