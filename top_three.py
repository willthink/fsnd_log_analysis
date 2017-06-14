
import psycopg2

def init_db():
	conn = psycopg2.connect("dbname=news")
	cur = conn.cursor()
	cur.execute("SELECT path, count(*) AS num FROM log WHERE path LIKE '/article/%' GROUP BY path ORDER BY num DESC LIMIT 3")
	cur.close()
	conn.close()

init_db()

	