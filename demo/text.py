import multiprocessing
import time

def text():
    while True:
        print("----1----")
        time.sleep(1)
def  text2():
    while True:
        print("----2----")
        time.sleep(1)

def main():
    p1 = multiprocessing.Process(target = text)
    p2 = multiprocessing.Process(target = text2)
    p1.start()
    p2.start()

if __name__ == '__main__':
    main()