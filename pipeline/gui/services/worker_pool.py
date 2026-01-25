import queue
import threading
import logging

class WorkerPool:
    """
    A simple, thread-safe worker pool with graceful shutdown
    and task completion tracking.
    """

    _SENTINEL = object()

    def __init__(self, num_workers=2):
        self.tasks = queue.Queue()
        self.num_workers = num_workers
        self.workers = []

        for i in range(num_workers):
            t = threading.Thread(
                target=self.worker_loop,
                daemon=True,
                name=f"Worker-{i+1}"
            )
            t.start()
            self.workers.append(t)

    def worker_loop(self):
        while True:
            task = self.tasks.get()

            # Sentinel means shutdown
            if task is self._SENTINEL:
                self.tasks.task_done()
                break

            func, args = task

            try:
                logging.info(f"[WorkerPool] Running task {func.__name__}")
                func(*args)
            except Exception as e:
                logging.error(f"[WorkerPool] Worker error: {e}")
            finally:
                self.tasks.task_done()

    def submit(self, func, *args):
        """Submit a task to the pool."""
        self.tasks.put((func, args))

    def wait_completion(self):
        """Block until all tasks are finished."""
        self.tasks.join()

    def shutdown(self):
        """Gracefully stop all workers."""
        # Send one sentinel per worker
        for _ in range(self.num_workers):
            self.tasks.put(self._SENTINEL)

        # Wait for workers to exit
        for t in self.workers:
            t.join()

        logging.info("[WorkerPool] Shutdown complete")
