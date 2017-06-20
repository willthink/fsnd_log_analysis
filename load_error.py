import psycopg2

DBNAME="news"
conn = psycopg2.connect(dbname=DBNAME)

def create_error_view():
  cur = conn.cursor()
  cur.execute(" \
   create view error_view as \
   select date(time) as day, count(*) as num , status \
   from log \
   where status like '404%' \
   group by date(time), status \
  ")
  cur.close()
def create_total_view():
  cur = conn.cursor()
  cur.execute(" \
   create view total_view as \
   select date(time) as day, count(*) as num \
   from log \
   group by date(time)\
  ")
  cur.close()


def load_errors():
  cur = conn.cursor()
  cur.execute(" \
   select error_view.day, error_view.num, error_view.num * 100/ total_view.num::float as error_rate  from error_view left join total_view on \
   error_view.day = total_view.day \
   where error_view.num * 100 /total_view.num::float > 1 \
  ")
  return cur.fetchall()
  cur.close()
  conn.close()

def print_rets(rets):
  for ret in rets:
    print ('{} {} {}'.format(ret[0], ret[1] ,ret[2]))     

create_error_view()
create_total_view()
rets = load_errors()
print_rets(rets)