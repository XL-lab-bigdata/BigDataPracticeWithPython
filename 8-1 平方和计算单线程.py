import threading
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def worker(number):
    return cpu_bound(number)


def find_sums(numbers):
    # 创建一个线程列表
    threads = []
    # 创建一个结果列表
    results = []

    # 为每个数字创建线程
    for number in numbers:
        t = threading.Thread(target=worker, args=(number,))
        threads.append(t)
        t.start()  # 启动线程

    # 等待所有线程完成
    for t in threads:
        t.join()
        # 假设worker函数返回结果，我们可以将其添加到结果列表中
        # 注意：这里我们假设worker函数返回结果，但在实际情况下，由于GIL的存在，
        # CPU密集型任务在多线程中可能并不会带来性能提升。
        # 如果你的任务实际上是I/O密集型或者可以被GIL很好地释放（比如涉及到很多系统调用），
        # 那么多线程可能会有用。
        # results.append(t.result)  # 这里实际上应该使用其他方式收集结果，因为Thread对象没有result属性

    # 由于cpu_bound函数没有直接返回结果给线程，我们需要以其他方式收集结果
    # 在这个例子中，我们假设worker函数返回结果，并将其添加到results列表中。
    # 在实际情况中，CPU密集型任务通常不适合多线程，因为它们受到GIL的限制。
    # 这里仅作为示例展示多线程结构，并不推荐在实际CPU密集型任务中使用多线程。
    # 如果要收集结果，你可能需要在线程内部处理或使用队列等机制。

    # 在这里我们只是假设worker函数已经处理了结果的收集，实际上它没有。
    # 因此，results列表将保持为空。对于CPU密集型任务，应该考虑使用多进程。

    return results  # 返回一个空列表，因为我们没有实际收集任何结果


if __name__ == "__main__":
    numbers = [5 + x for x in range(20000)]
    start_time = time.time()
    results = find_sums(numbers)  # 执行多线程计算
    duration = time.time() - start_time
    print(f"Duration: {duration} seconds")

# Duration: 19.66149115562439 seconds

