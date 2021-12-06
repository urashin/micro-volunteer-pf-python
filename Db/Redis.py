from redis import StrictRedis
import config

redis: StrictRedis = StrictRedis(host=config.redis_host, port=config.redis_port, db=0)
