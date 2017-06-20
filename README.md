# fsnd_log_analysis

## Overview
This project is for Udacity Full Stack Web Developer Nanodegree Log Analysis Project.  
##  Instruction to Run 
### Prepare Environment 
```
1. Install Vagrant virtual machine 
2. Download data
3. Import data 
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

### 2. Who are the most popular article authors of all time?
```
python log_analysis.py 2
```

### 3. On which days did more than 1% of requests lead to errors? 
```
python log_analysis.py 3
```
