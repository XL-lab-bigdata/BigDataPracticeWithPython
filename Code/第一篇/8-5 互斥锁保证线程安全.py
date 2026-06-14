import threading

num = 0
lock = threading.Lock()

def add():
	global num
	lock.acquire()
	for i in range(1000000):
		num += 1
	lock.release()

def desc():
	global num
	lock.acquire()
	for i in range(1000000):
		num -= 1
	lock.release()

if __name__ == '__main__':
	thread1 = threading.Thread(target=add)
	thread2 = threading.Thread(target=desc)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

	print(num)
