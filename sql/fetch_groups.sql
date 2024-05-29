select
   o.id, 
   o.tag as group_tag,
   count(b.id) block_count,
   (select count(*) from prompt_responses pr where pr.block_id = b.id) as prompt_count
  FROM
   groups o
	join blocks b on b.group_id = o.id
group by
   o.id;