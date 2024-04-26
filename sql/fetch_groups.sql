select
   o.id, 
   o.arguments,
   o.tag,
   count(b.id) block_count
  FROM
     groups o
	 join blocks b on b.group_id = o.id
group by
   o.id;