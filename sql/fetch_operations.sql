select
   o.id, 
   o.arguments,
   count(b.id) block_count
  FROM
     operations o
	 join blocks b on b.operation_id = o.id
group by
   o.id;