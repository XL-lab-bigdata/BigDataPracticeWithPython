import multiprocessing
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        # 使用 list() 来确保获取所有结果
        results = list(pool.map(cpu_bound, numbers))
    return results


if __name__ == "__main__":
    numbers = [5 + x for x in range(20000)]
    start_time = time.time()
    results = find_sums(numbers)  # 存储结果
    duration = time.time() - start_time
    print(f"Duration: {duration} seconds")
    #
    #print(results)

#Duration: 3.9019901752471924 seconds

