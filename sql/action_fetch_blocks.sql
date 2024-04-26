select 
   b.id,
   o.tag as group_tag,
   b.tag as block_tag,
   b.block
 FROM
   groups o
   join blocks b on b.group_id = o.id
   join current_group co
WHERE
   b.tag like ? and 
   b.group_id = co.id
order by
    b.group_id,
    b.id