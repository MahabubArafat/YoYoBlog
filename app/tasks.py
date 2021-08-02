import time

def example(seconds):
    print("Task Starting")
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print("Task Complete")