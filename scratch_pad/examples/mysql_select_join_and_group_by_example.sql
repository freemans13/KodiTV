-- http://www.mysqltutorial.org/mysql-inner-join.aspx
select
  g.genre,
  count(g.genre)
from
  shows h
  inner join show_genre_map m on h.show_id = m.show_id
  inner join genres g on m.genre_id = g.genre_id
group by g.genre
order by 2 desc
;

select
  channel,
  count(channel)
from
  shows
group by channel
order by 2 desc
;
