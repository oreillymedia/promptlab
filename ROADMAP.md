- Create new group based on a filter
- Provide a searchacble name by block
- rewrite readme

# Replace weird selection logi for blocks with a `where` clause

# Computing metadata

- Start with a set of blocks
- Apply a prompt to each block, This creates new entries in the prompts table
- pull those prompts back into the block table
-

Group block parent text
1 1 0 Cats are funny. Elephants are big. Dogs are loyal.
2 1 1 Cats are funny.
2 2 1 Elephants are big.
2 3 1 Dogs are loyal.

Select the key trait from {{block}}
