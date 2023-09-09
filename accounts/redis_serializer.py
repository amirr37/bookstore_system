import redis
import pickle

# Connect to your Redis server
redis_url = 'redis://localhost:6379/0'  # Update with your Redis server URL
redis_client = redis.from_url(redis_url)

# Specify the Redis keys for your Circuit Breaker instances
keys = ["service3", "service2", "service1"]  # Update with unique keys

for key in keys:
    # Retrieve the serialized data from Redis for each instance
    serialized_data = redis_client.get(key)

    if serialized_data:
        # Deserialize the data using pickle
        circuit_breaker_data = pickle.loads(serialized_data)

        # Now, you can access and print the attributes of each Circuit Breaker instance
        print("Service Name:", circuit_breaker_data.get('service_name'))
        print("Max Failures:", circuit_breaker_data.get('max_failures'))
        print("Reset Timeout:", circuit_breaker_data.get('reset_timeout'))
        print("Failures:", circuit_breaker_data.get('failures'))
        print("Last Failure Time:", circuit_breaker_data.get('last_failure_time'))
        print("Circuit Open:", circuit_breaker_data.get('circuit_open'))
        print("\n")  # Add a separator between instances
    else:
        print(f"No data found in Redis for key: {key}")
