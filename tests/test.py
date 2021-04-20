import multiprocessing as mp 
from datetime import datetime
import numpy as np 
import os
import soundfile as sf
class testdata:
    def __init__(self):
        self.data = mp.Queue()
        self.data.put('lol ok')
    
    def task1(self):
        print(f"task 1 is running at {datetime.now().time()} with and processID {os.getpid()}")
        data = self.data.get()
        data = data + ' lmao'
        self.data.put(data)

    def task2(self):
        print(f"task 2 is running at {datetime.now().time()} with and processID {os.getpid()}")
        data = self.data.get()
        data = data + ' bruh'
        self.data.put(data)


if __name__ == "__main__":
    test = testdata()
    p1 = mp.Process(target=test.task1)
    p2 = mp.Process(target=test.task2)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(test.data.get())
    print("Done!")
    print(test.data.get())




