create table if not exists groups (
    id integer primary key autoincrement,
    arguments text,
    tag text,
    created_at datetime DEFAULT CURRENT_TIMESTAMP
);

create table if not exists blocks (
    id integer primary key autoincrement,
    tag text,
    group_id int,   
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    parent_id int DEFAULT 0,
    block text,
    CONSTRAINT fk_group
        FOREIGN KEY (group_id)
        REFERENCES groups(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_parent
        FOREIGN KEY (parent_id)
        REFERENCES blocks(id)
        
);

create table if not exists prompt_responses (
    id integer primary key autoincrement,
    prompt_log_id int,
    block_id int,
    prompt_hash text,
    response text,
    elapsed_time_in_seconds float,
    created_at datetime DEFAULT CURRENT_TIMESTAMP
);

create table if not exists prompt_log (
    id integer primary key autoincrement,
    prompt_fn text,
    prompt text,
    arguments text,
    tag text,
    created_at datetime DEFAULT CURRENT_TIMESTAMP
);


create table if not exists current_group as 
    select 0 as id;



create table if not exists metadata (
    id integer primary key autoincrement,
    block_id int,  
    key text,
    value text, 
    CONSTRAINT fk_block
        FOREIGN KEY (block_id)
        REFERENCES blocks(id)
        ON DELETE CASCADE
);
