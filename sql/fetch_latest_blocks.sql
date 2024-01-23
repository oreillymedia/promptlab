select 
   b.*,
   o.operation,
   o.description
 FROM
    operations o
	join blocks b on b.operation_id = o.id
WHERE
   b.tag like ? and 
   b.operation_id = (select max(id) from operations)
order by
    b.operation_id,
    b.id
