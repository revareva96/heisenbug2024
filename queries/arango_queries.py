check_data = """
    with Dirs
    for d in Dirs
        filter d.name == 'dir'
        limit 1
        return d
"""

create_dirs = """
    with Dirs 
    for dir_name in @dirs
        insert {'name': dir_name} in Dirs
        return NEW
"""

create_edges = """
    with Subdirs
    insert {'_from': @_from, '_to': @_to} into Subdirs
"""

get_dirs = """
    with Dirs, Subdirs
    let dir = (for d in Dirs
    filter d.name == @name
    return d)[0]
    for v in 1..1000
        outbound dir Subdirs
        return v.name
"""