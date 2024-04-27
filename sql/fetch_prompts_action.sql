SELECT
    p.id,
    l.tag as prompt_tag,
    p.block_id,
    b.tag  as block_tag,
    l.prompt_fn,
    p.response
FROM 
     prompt_responses p
	 join prompt_log l on l.id = p.prompt_log_id
	 join blocks b on b.id = p.block_id
WHERE
   l.tag like ?