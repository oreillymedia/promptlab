SELECT
   pr.id as prompt_id,
   b.group_id,
   pr.block_id,
   b.parent_id as block_parent_id,
   g.tag as 
   group_tag,
   b.tag as block_tag,
   pl.tag as prompt_tag,
   pr.response,
   pr.elapsed_time_in_seconds
 FROM
   prompt_responses pr
   join blocks b on b.id = pr.block_id 
   join prompt_log pl on pl.id = pr.prompt_log_id
   join groups g on g.id = b.group_id
   join current_group cg on cg.id = b.group_id
