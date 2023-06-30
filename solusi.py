from multiprocessing import Process

def jobpln():
    while True:
        ac_voltdown()
        time.sleep(5)

def jobbaterai():
    while True:
        send_battery_status()
        time.sleep(1)

if __name__ == '__main__':
    process1 = Process(target=jobpln)
    process2 = Process(target=jobbaterai)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
