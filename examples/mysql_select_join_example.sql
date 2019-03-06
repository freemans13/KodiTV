-- http://www.mysqltutorial.org/mysql-inner-join.aspx
select
  h.show_id,
  h.title,
  g.genre
from
  shows h
  inner join show_genre_map m on h.show_id = m.show_id
  inner join genres g on m.genre_id = g.genre_id
order by
  h.show_id,
  h.title,
  g.genre;