import threading

num = 0
lock = threading.Lock()

def add():
	global num
	with lock:
		# 自动加锁
		for i in range(1000000):
			num += 1
		# 自动解锁

def desc():
	global num
	with lock:
		# 自动加锁
		for i in range(1000000):
			num -= 1
		# 自动解锁

if __name__ == '__main__':
	thread1 = threading.Thread(target=add)
	thread2 = threading.Thread(target=desc)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

	print(num)