import time


class CircuitBreaker:
    def __init__(self, max_failures=5, reset_timeout=1800):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.circuit_open = False

    def is_open(self):
        if self.circuit_open:
            if time.time() - self.last_failure_time >= self.reset_timeout:
                self.reset()
            return True
        return False

    def increment_failures(self):
        self.failures += 1
        if self.failures >= self.max_failures:
            self.open()

    def open(self):
        self.circuit_open = True
        self.last_failure_time = time.time()

    def reset(self):
        self.failures = 0
        self.circuit_open = False
