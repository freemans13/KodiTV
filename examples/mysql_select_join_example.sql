-- http://www.mysqltutorial.org/mysql-inner-join.aspx
select
  h.history_id,
  h.title,
  g.genre
from
  history h
  inner join history_genre_map m on h.history_id = m.history_id
  inner join genres g on m.genre_id = g.genre_id
order by
  h.history_id,
  h.title,
  g.genre;