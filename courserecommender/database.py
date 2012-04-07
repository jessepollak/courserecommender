from urlparse import urlparse

AVAILABLE_ENGINES = ()

try:
    import psycopg2
    AVAILABLE_ENGINES += ("postgres",)
except ImportError:
    pass

try:
    import sqlite3
    AVAILABLE_ENGINES += ("sqlite",)
except ImportError:
    pass

if not AVAILABLE_ENGINES:
    raise RuntimeError("No available database engines!")

class SqliteConfig:
	def __init__(self, path):
		self.path = path
		if path == '': self.path == ":memory:"

	def connection(self):
		return sqlite3.connect(self.path)

class PostgresConfig:
	def __init__(self, url):
		self.opts = {
			user: url.username,
			password: url.password,
			host: url.hostname,
			port: url.port,
			database: os.path.basename(url.path),
		}
	def connection(self):
		return psycopg2.connect(**self.opts)

def get_configuration(url):
	parsed_url = urlparse(url)
	if parsed_url.scheme not in AVAILABLE_ENGINES:
	    raise RuntimeError("Database URI scheme requires an engine that "
	        "is not available!")
	if parsed_url.scheme == "sqlite":
		return SqliteConfig(parsed_url.path)
	elif parsed_url.scheme == "postgres":
		return PostgresConfig(parsed_url)