with recursive
   cte as (
     select id, parent_id from blocks where id = 71
     union all
     select b.id, b.parent_id from blocks b
     join cte on b.id = cte.parent_id
   )
 select * from cte;