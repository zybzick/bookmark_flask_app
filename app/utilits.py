def autoget(list_, dict_):
    return [dict_.get(key) if key in dict_ else None for key in list_]
