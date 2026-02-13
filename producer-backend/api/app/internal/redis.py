import redis
from app.internal.settings import RedisSessionManagerSettings

redis_pool = redis.ConnectionPool(
    host=RedisSessionManagerSettings.host,
    port=RedisSessionManagerSettings.port,
    db=RedisSessionManagerSettings.db
)

redis_client = redis.Redis(connection_pool=redis_pool)