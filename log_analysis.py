#!/usr/bin/env python
import psycopg2
import sys

DBNAME = "news"
conn = psycopg2.connect(dbname=DBNAME)


def top_three():
    cur = conn.cursor()
    cur.execute("""
        select articles.title, path_view.num
        from articles join path_view
        on path_view.path = concat('/article/', articles.slug)
        order by path_view.num desc
        limit 3""")

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def pop_author():
    cur = conn.cursor()
    cur.execute("""
        select authors.name, sum(author_view.num) as sum
        from authors join author_view
        on authors.id = author_view.author
        group by authors.name
        order by sum desc""")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def load_errors():
    cur = conn.cursor()
    cur.execute("""
       select to_char(error_view.day, 'Mon dd, yyyy'),
       concat((round(error_view.num * 100 / total_view.num::decimal, 2)::text),
               '% errors')
       as error_rate
       from error_view left join total_view on
       error_view.day = total_view.day
       where error_view.num * 100 / total_view.num::float > 1""")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def print_rets(rets):
    for ret in rets:
        print ('{} -- {}'.format(ret[0], ret[1]))


def main(input):
    if(input[1] == '1'):
        rets = top_three()
        print_rets(rets)
    elif(input[1] == '2'):
        rets = pop_author()
        print_rets(rets)
    elif(input[1] == '3'):
        rets = load_errors()
        print_rets(rets)
    else:
        print 'Usage: python log_analysis [1/2/3]'

if len(sys.argv) == 2:
    main(sys.argv)
else:
    print 'Usage: python log_analysis [1/2/3]'
