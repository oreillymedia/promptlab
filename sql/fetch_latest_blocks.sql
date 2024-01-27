select 
   b.*
 FROM
   operations o
	join blocks b on b.operation_id = o.id
   join current_operation co
WHERE
   b.tag like ? and 
   b.operation_id = co.operation
order by
    b.operation_id,
    b.id
