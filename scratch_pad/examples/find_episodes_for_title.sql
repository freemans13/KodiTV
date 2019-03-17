select
  s.show_ID,
  e.plot
from shows s
    inner join episodes e on s.show_ID = e.show_ID
where s.title = "Family Guy";