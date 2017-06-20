import psycopg2

DBNAME = "news"
conn = psycopg2.connect(dbname=DBNAME)


def create_view():
    cur = conn.cursor()
    cur.execute(
        "create view path_view as \
         select path, count(*) as num \
         from log \
         where path like '/article/%' \
         group by path  \
         order by num desc")
    cur.close()


def top_three():
    cur = conn.cursor()
    cur.execute(
        "select articles.title, path_view.num \
        from articles join path_view \
        on path_view.path = concat('/article/', articles.slug) \
        order by path_view.num desc \
        limit 3")

    return cur.fetchall()
    cur.close()
    conn.close()


def print_rets(rets):
    for ret in rets:
        print ('{} {}'.format(ret[0], ret[1]))

create_view()
rets = top_three()
print_rets(rets)
