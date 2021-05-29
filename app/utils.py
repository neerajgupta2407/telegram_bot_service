
def lis_to_str_with_indx(lis):
    return "\n".join([f"{idx + 1}. {b}" for idx, b in enumerate(lis)])


def lis_to_str(lis):
    return "\n".join([f"{b}" for idx, b in enumerate(lis)])


def remove_extra_delimiter(query_str, delimeter=" "):
    delim = delimeter
    query_str = delim.join([a for a in query_str.lower().split(delim) if a != ""])
    return query_str


def insert_top(lis, item):
    # inserts item at top if exists.
    if item in lis:
        lis.remove(item)
    lis.insert(0, item)
    return lis
