SELECT
    p.block_id as parent,
    p.response as block,
    l.tag
from 
    prompt_responses p
    join prompt_log l on l.id = p.prompt_log_id
WHERE
   l.tag like ?