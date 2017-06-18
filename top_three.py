import psycopg2

DBNAME="news"
conn = psycopg2.connect(dbname=DBNAME)

def create_view():
  cur = conn.cursor()
  cur.execute(
    "CREATE VIEW path_view AS \
    SELECT path, COUNT(*) AS num FROM log WHERE \
    path LIKE '/article/%' \
    GROUP BY path  \
    ORDER BY num desc")
  cur.close()

def top_three():
  cur = conn.cursor()
  cur.execute(
    " SELECT articles.title, path_view.num FROM articles JOIN path_view ON \
      path_view.path = CONCAT('/article/', articles.slug) \
      ORDER BY path_view.num desc \
      LIMIT 3")

  return cur.fetchall()
  cur.close()
  conn.close()

def print_rets(rets):
  for ret in rets:
    print ('{} {}'.format(ret[0], ret[1]))     

create_view()
rets = top_three()
print_rets(rets)