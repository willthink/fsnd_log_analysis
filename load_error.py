import psycopg2

DBNAME = "news"
conn = psycopg2.connect(dbname=DBNAME)


def create_view():
    cur = conn.cursor()
    cur.execute(" \
       create or replace view status_view as \
       select date(time) as day, count(*) as num, status \
       from log \
       group by date(time), status")
    cur.close()


def create_error_view():
    cur = conn.cursor()
    cur.execute(" \
       create view error_view as \
       select day, num , status \
       from status_view \
       where status like '404%' \
       group by day, status, num")
    cur.close()


def create_total_view():
    cur = conn.cursor()
    cur.execute(" \
       create view total_view as \
       select day, sum(num) as num\
       from status_view \
       group by day")
    cur.close()


def load_errors():
    cur = conn.cursor()
    cur.execute(" \
       select to_char(error_view.day, 'Mon dd, yyyy'), \
       round( \
           error_view.num * 100 / total_view.num::decimal, 2)::text\
      as error_rate  \
       from error_view left join total_view on \
       error_view.day = total_view.day \
       where error_view.num * 100 / total_view.num::float > 1")
    return cur.fetchall()
    cur.close()
    conn.close()


def print_rets(rets):
    for ret in rets:
        print ('{} -- {}% errors'.format(ret[0], ret[1]))


create_view()
create_total_view()
create_error_view()
rets = load_errors()
print_rets(rets)
