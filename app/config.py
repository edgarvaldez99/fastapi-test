from decouple import config as environ  # type: ignore

dburl = str(environ("DATABASE_URL", "localhost:5432"))
dbuser = str(environ("DATABASE_USER", "test"))
dbpasw = str(environ("DATABASE_PASS", "test"))
dbname = str(environ("DATABASE_NAME", "test"))
dbtype = str(environ("DATABASE_TYPE", "postgresql"))

API_BASE_URL = ""

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{dbuser}:{dbpasw}@{dburl}/{dbname}"
