SELECT
   b.id as block_id,
   b.tag as block_tag,
   b.parent_id as parent_block_id,
   g.id as group_id,
   g.tag as group_tag,
   b.block as block,
   b.token_count as token_count
 from
  groups g
  join current_group cg on cg.id = g.id
  join blocks b on b.group_id = g.id