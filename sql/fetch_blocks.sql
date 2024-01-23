select 
   b.*,
   o.operation,
   o.description
 FROM
    operations o
	join blocks b on b.operation_id = o.id
WHERE
   b.tag like ?
order by
    b.operation_id,
    b.position
