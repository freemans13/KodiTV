select s.show_id, e.season, max(e.episode) last_episode
from shows s
       inner join episodes e on s.show_id = e.show_id
where s.title = 'The Jonathan Ross Show'
group by s.show_id, e.season
order by e.season desc
limit 1;