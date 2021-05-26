def list_to_str(lis):
    return "\n".join(lis)

def list_to_str_with_idx(lis):
    return "\n".join([f"{idx + 1}: {l}" for idx, l in enumerate(lis)])