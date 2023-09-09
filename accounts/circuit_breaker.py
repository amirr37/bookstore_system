import time
import redis
import pickle

class CircuitBreaker:
    def __init__(self, service_name, max_failures=5, reset_timeout=1800, redis_url='redis://localhost:6379/0'):
        self.service_name = service_name
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time = None
        self.circuit_open = False
        self.redis_url = redis_url
        self.redis_key = f'circuit_breaker_state_{service_name}'  # Use a unique Redis key for each service
        self.redis_client = redis.from_url(redis_url)

        # Load state from Redis during initialization
        self.save_state()

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

        # Save state in Redis
        self.save_state()

    def open(self):
        self.circuit_open = True
        self.last_failure_time = time.time()

        # Save state in Redis
        self.save_state()

    def reset(self):
        self.failures = 0
        self.circuit_open = False

        # Save state in Redis
        self.save_state()

    def save_state(self):
        # Create a dictionary of attributes to save
        state_to_save = {
            'service_name': self.service_name,
            'max_failures': self.max_failures,
            'reset_timeout': self.reset_timeout,
            'failures': self.failures,
            'last_failure_time': self.last_failure_time,
            'circuit_open': self.circuit_open,
        }

        # Serialize the state dictionary and save it in Redis
        serialized_state = pickle.dumps(state_to_save)
        self.redis_client.set(self.service_name, serialized_state)

    # def load_state(self):
    #     # Attempt to load the CircuitBreaker state from Redis
    #     serialized_state = self.redis_client.get(self.redis_key)
    #     if serialized_state:
    #         # Deserialize the state dictionary
    #         state_to_load = pickle.loads(serialized_state)
    #
    #         # Update the current instance's attributes from the loaded state
    #         self.max_failures = state_to_load['max_failures']
    #         self.reset_timeout = state_to_load['reset_timeout']
    #         self.failures = state_to_load['failures']
    #         self.last_failure_time = state_to_load['last_failure_time']
    #         self.circuit_open = state_to_load['circuit_open']
