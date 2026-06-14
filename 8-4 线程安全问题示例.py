import threading
#对于一个全局变量 num，初始值为0，开启两条线程分别对 num 进行一百万次加1和一百万次减1，然后打印最后的结果
num = 0

def add():
	global num
	for i in range(1000000):
		num += 1

def desc():
	global num
	for i in range(1000000):
		num -= 1

if __name__ == '__main__':
	thread1 = threading.Thread(target=add)
	thread2 = threading.Thread(target=desc)

	thread1.start()
	thread2.start()

	thread1.join()
	thread2.join()

	print(num)
