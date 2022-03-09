import math, time
import os
import concurrent.futures
import logging


def create_logger(name: str, file_name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(file_name, mode="w")
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = create_logger("medium", os.path.join("hw_4", "artifacts", "log.log"))


def integrate_body(f, a, step, n_iter, task_number):
    acc = 0
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_threads(f, a, b, *, n_jobs, n_iter=20_000_000):
    start = time.time()
    acc = 0.0
    step = (b - a) / n_iter
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_body, f, a + i * (b - a) / n_jobs, step, n_iter // n_jobs, i + 1) for i in range(n_jobs)]
        for future in concurrent.futures.as_completed(futures):
            acc += future.result()
    logger.info(f"Time on {n_jobs} threads: {time.time() - start:.4f}s, result={acc}")
    return acc


def integrate_processes(f, a, b, *, n_jobs, n_iter=20_000_000):
    start = time.time()
    acc = 0.0
    step = (b - a) / n_iter
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(integrate_body, f, a + i * (b - a) / n_jobs, step, n_iter // n_jobs, i + 1) for i in range(n_jobs)]
        for future in concurrent.futures.as_completed(futures):
            acc += future.result()
    logger.info(f"Time on {n_jobs} processes: {time.time() - start:.4f}s, result={acc}")
    return acc


if __name__ == "__main__": 
    cpu_num = 4
    for i in range(1, 2 * cpu_num + 1):
        integrate_threads(math.cos, 0, math.pi / 2, n_jobs=i)
    for i in range(1, 2 * cpu_num + 1):
        integrate_processes(math.cos, 0, math.pi / 2, n_jobs=i)
