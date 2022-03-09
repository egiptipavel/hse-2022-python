import time
from threading import Thread
from multiprocessing import Process


def fib(n):
    res = []
    a = 0
    b = 1
    while n != 0:
        res.append(a)
        a = a + b
        b = a - b
        n = n - 1
    return res


def time_on_threads(n: int = 100_000, num_of_threads = 10, prefix: str = "Time on threads:") -> str:
    threads = []
    for _ in range(num_of_threads):
        threads.append(Thread(target=fib, args=(n,)))
    start = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return f"{prefix} {time.time() - start:.4f}s"


def time_on_processes(n: int = 100_000, num_of_processes: int = 10, prefix: str = "Time on processes:") -> str:
    processes = []
    for _ in range(num_of_processes):
        processes.append(Process(target=fib, args=(n,)))
    start = time.time()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    return f"{prefix} {time.time() - start:.4f}s"


def time_at_sync_start(n: int = 100_000, num_of_starts: int = 10, prefix: str = "Time at synchronous start:") -> str:
    start = time.time()
    for _ in range(num_of_starts):
        fib(n)
    return f"{prefix} {time.time() - start:.4f}s"


if __name__ == "__main__":
    print(time_at_sync_start())
    print(time_on_threads())
    print(time_on_processes())
