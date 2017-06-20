import psycopg2

DBNAME="news"
conn = psycopg2.connect(dbname=DBNAME)

def create_path_view():
  cur = conn.cursor()
  cur.execute(
    "CREATE VIEW path_view AS \
    SELECT path, COUNT(*) AS num FROM log WHERE \
    path LIKE '/article/%' \
    GROUP BY path  \
    ORDER BY num desc")
  cur.close()

def create_author_view():
  cur = conn.cursor()
  cur.execute(
  " CREATE VIEW author_view AS \
    SELECT articles.title as title, articles.author as author, path_view.num as num FROM articles JOIN path_view ON \
    path_view.path = CONCAT('/article/', articles.slug) \
    ORDER BY path_view.num desc")
  cur.close()

def pop_author():
  cur = conn.cursor()
  cur.execute(
  " \
    select authors.name, sum(author_view.num) as sum from authors join author_view on \
    authors.id = author_view.author \
    group by authors.name \
    order by sum desc \
  ")

  return cur.fetchall()
  cur.close()
  conn.close()

def print_rets(rets):
  for ret in rets:
    print ('{} -- {} views'.format(ret[0], ret[1]))     

create_path_view()
create_author_view()
rets = pop_author()
print_rets(rets)
