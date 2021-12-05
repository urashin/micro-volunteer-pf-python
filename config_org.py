from os import environ

# rename this file into config.py

http_host = environ.get("HTTP_HOST", '0.0.0.0')
http_port = environ.get("HTTP_PORT", 8000)

api_web_prefix = environ.get("API_WEB_PREFIX", "/v1/user")

line_messaging_web_prefix = environ.get("LINE_MESSAGING_WEB_PREFIX", "/messaging")
line_messaging_channel_access_token = environ.get("LINE_MESSAGING_CHANNEL_ACCESS_TOKEN", "...")
line_messaging_channel_secret = environ.get("LINE_MESSAGING_CHANNEL_SECRET", "...")

redis_host = environ.get("REDIS_HOST", "redis.server")
redis_port = environ.get("REDIS_PORT", 6379)

mysql_host = environ.get("MYSQL_HOST", 'mysql.server')
mysql_port = environ.get("MYSQL_PORT", 3306)
mysql_user = environ.get("MYSQL_USER", 'volunteer')
mysql_password = environ.get("MYSQL_PASSWORD", 'volunteer')
mysql_database = environ.get("MYSQL_DATABASES", 'volunteerdb')

java_host = environ.get("JAVA_HOST", 'http://localhost:8080')
deeplink_host = environ.get("DEEPLINK_HOST", 'http://example.com')
