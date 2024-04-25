select
   l.id, 
   l.prompt_fn,
   l.tag, 
   l.created_at,
   (select count(*) from prompt_responses where prompt_log_id = l.id) as response_count
from 
   prompt_log l
where
   tag like ?
order by
   created_at desc;