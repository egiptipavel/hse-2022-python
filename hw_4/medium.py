import math, time
import os
import concurrent.futures
import logging


def create_logger(name: str, file_name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(file_name, mode="w")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = create_logger("medium", os.path.join("hw_4", "artifacts", "log.log"))


def integrate_body(f, a, step, n_iter, task_number):
    logger.info(f"Task {task_number} start")
    acc = 0
    for i in range(n_iter):
        acc += f(a + i * step) * step
    logger.info(f"Task {task_number} stop")
    return acc


def integrate_threads(f, a, b, *, n_jobs, n_iter=20_000_000):
    acc = 0.0
    step = (b - a) / n_iter
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_body, f, a + i * (b - a) / n_jobs, step, n_iter // n_jobs, i + 1) for i in range(n_jobs)]
        for future in concurrent.futures.as_completed(futures):
            acc += future.result()
    return acc


def integrate_processes(f, a, b, *, n_jobs, n_iter=20_000_000):
    acc = 0.0
    step = (b - a) / n_iter
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_body, f, a + i * (b - a) / n_jobs, step, n_iter // n_jobs, i + 1) for i in range(n_jobs)]
        for future in concurrent.futures.as_completed(futures):
            acc += future.result()
    return acc


if __name__ == "__main__": 
    cpu_num = 8
    logger.info("Threads")
    for i in range(1, 2 * cpu_num + 1):
        start = time.time()
        integrate_threads(math.cos, 0, math.pi / 2, n_jobs=i)
        print(f"Time on {i} threads: {time.time() - start:.4f}s")
    print()
    logger.info("Processes")
    for i in range(1, 2 * cpu_num + 1):
        start = time.time()
        integrate_processes(math.cos, 0, math.pi / 2, n_jobs=i)
        print(f"Time on {i} processes: {time.time() - start:.4f}s")
