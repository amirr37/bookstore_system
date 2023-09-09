import time
import redis


class CircuitBreaker:
    def __init__(self,  max_failures=5, reset_timeout=1800, redis_url='redis://foobared@localhost:6379/0'):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.circuit_open = False
        # self.redis_url = redis_url
        # self.redis_client = redis.from_url(redis_url)
        self.available_services = []

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

        # Save failures count in Redis
        # self.redis_client.setex('failures_count', self.reset_timeout, self.failures)

    def open(self):
        self.circuit_open = True
        self.last_failure_time = time.time()

        # Save circuit state in Redis
        # self.redis_client.set('circuit_open', '1')

    def reset(self):
        self.failures = 0
        self.circuit_open = False

        # Reset data in Redis
        # self.redis_client.delete('failures_count')
        # self.redis_client.delete('circuit_open')
