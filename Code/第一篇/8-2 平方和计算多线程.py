import concurrent.futures
import time

def cpu_bound(number):
    return sum(i * i for i in range(number))

def find_sums(numbers): # 建立最大线程数为5的线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(cpu_bound, numbers)

if __name__ == "__main__":
    numbers = [5 + x for x in range(20000)]
    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds")

