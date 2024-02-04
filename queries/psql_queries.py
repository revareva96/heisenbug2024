table_exist = """
    select * from information_schema.tables where table_name=%s
"""

create_dirs = """
    CREATE TABLE %s
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    "name" text,
    PRIMARY KEY (id)
);
"""

create_edges = """
    CREATE TABLE %s 
(
    edge_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 ),
    head_id integer references dirs (id),
    tail_id integer references dirs (id),
    PRIMARY KEY (edge_id)
);
    CREATE INDEX edges_heads ON edges_dirs (head_id);
    CREATE INDEX edges_tails ON edges_dirs (tail_id);
"""

get_recursive_data = """
    with recursive 
    in_dirs(id) as (
        select id from dirs where name = %s
        union 
        select e.tail_id from edges_dirs as e
        join in_dirs e_dirs
        on e.head_id = e_dirs.id
    )
    select dirs.name from in_dirs
    join dirs
    on in_dirs.id = dirs.id;
"""
