/* maps grouped by map size */
select map.map_size, count(*)
from map
where map.id in (select map.id
                 from map
                          left join player p on map.id = p.map
                          join team t on t.id = p.team
                 group by map.id
                 having count(p.id) in (1, 2, 3, 4, 5, 6, 7, 8)
                    and count(t.id) in (1, 2, 3, 4, 5, 6, 7, 8))
group by map.map_size;

/* maps grouped by player number */
select c, count(*)
from (select count(*) as c
      from map
               left join player p on map.id = p.map
               join team t on t.id = p.team
      where map.map_size in (36, 72, 108, 144, 180, 216, 252)
      group by map.id
      having count(p.id) in (1, 2, 3, 4, 5, 6, 7, 8)
         and count(t.id) in (1, 2, 3, 4, 5, 6, 7, 8))
group by c;

/* maps grouped by number of teams*/
select tid, count(*)
from (select t.id as tid
      from map
               left join player p on map.id = p.map
               join team t on t.id = p.team
      where map.map_size in (36, 72, 108, 144, 180, 216, 252)
      group by map.id
      having count(p.id) in (1, 2, 3, 4, 5, 6, 7, 8)
         and (select distinct p.team from player))
group by tid;
