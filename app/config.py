# FEED
FEED_URL = 'https://www.ctidoma.cz/export/cesko-digital'

# DB
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_USER = 'postgres'
POSTGRES_PASS = 'postgres'
POSTGRES_DB = 'feed_parser'

POSTGRES_DB_CONN = "postgresql://{}:{}@{}:5432/{}"\
    .format(POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
