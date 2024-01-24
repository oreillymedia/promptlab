create table if not exists operations (
    id integer primary key autoincrement,
    operation text,
    description text,
    arguments text,
    created_at datetime DEFAULT CURRENT_TIMESTAMP
);

create table if not exists blocks (
    id integer primary key autoincrement,
    tag text,
    operation_id int,   
    position int,
    token_count int,
    created_at datetime DEFAULT CURRENT_TIMESTAMP,
    block text,
    CONSTRAINT fk_operation
        FOREIGN KEY (operation_id)
        REFERENCES operations(id)
        ON DELETE CASCADE
);



