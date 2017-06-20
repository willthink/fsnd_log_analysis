# fsnd_log_analysis

## Overview
This project is for Udacity Full Stack Web Developer Nanodegree Log Analysis Project.  
##  Instruction to Run 
### Prepare Environment 

1. Install Vagrant virtual machine 
2. Download newsdata.sql from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
3. Import data by execute below command in virtual machine:
```
   psql -d news -f newsdata.sql
```

### Create Views 
```
create view path_view as 
        select path, count(*) as num from log where 
        path like '/article/%' 
        group BY path  
        order BY num desc;
```

```
create view author_view as 
        select articles.title as title, 
        articles.author as author, 
        path_view.num as num 
        from articles join path_view 
        on path_view.path = concat('/article/', articles.slug) 
        order by path_view.num desc;
```


```
create view error_view as 
       select date(time) as day, count (*) as num
       from log 
       where status like '404%' 
       group by day;
```

```
 create view total_view as 
       select date(time) as day, count(*) as num
       from log 
       group by day;
```


### 1. What are the most popular three articles of all time?
```
python log_analysis.py 1
```
This will show the top three most viewed article from database 
with article title and number of views 

Sample output 
```
Candidate is jerk, alleges rival -- 338647
Bears love berries, alleges bear -- 253801
Bad things gone, say good people -- 170098
```

### 2. Who are the most popular article authors of all time?

```
python log_analysis.py 2
```
This will list all the authors in the database with number of 
views for their articles, and order by views in desc 

Sample output
```
Ursula La Multa -- 507594
Rudolf von Treppenwitz -- 423457
Anonymous Contributor -- 170098
Markoff Chaney -- 84557
```


### 3. On which days did more than 1% of requests lead to errors? 
```
python log_analysis.py 3

This will list all the days which has more than 1% request errors 

```
Sample output 
```
Jul 17, 2016 -- 2.26% errors
```
