import redis

r = redis.Redis(
    host="localhost",
    port=6380,
    db=0,
)

try:
    response = r.ping()
    print("Redis is reachable:", response)
except redis.exceptions.ConnectionError as e:
    print("Redis connection failed:", e)
