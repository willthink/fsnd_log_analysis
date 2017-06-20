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

def most_pop_authors():
  cur = conn.cursor()
  cur.execute( 
   " SELECT articles.author, sum(path_view.num) FROM articles JOIN path_view ON \
     path_view.path = concat('/article/', articles.slug) \
     group by articles.author \
     order by path_view.num desc")
  return cur.fetchall()
  cur.close()
  conn.close()

def print_rets(rets):
  for ret in rets:
    print ('{} {}'.format(ret[0], ret[1]))     

create_view()
rets = most_pop_authors()
print_rets(rets)


#select authors.name , count(authors.name) as num from authors join articles on 
#authors.id = articles.author
#group by authors.name
#order by num desc;

