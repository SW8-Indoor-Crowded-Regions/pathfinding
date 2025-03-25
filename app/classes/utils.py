def dict_to_obj(data):
    """
    Recursively converts dictionaries (or lists of dictionaries) into objects
    for attribute-style access. (This is provided as a helper if needed.)
    """
    if isinstance(data, dict):
        from types import SimpleNamespace

        return SimpleNamespace(**{k: dict_to_obj(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_obj(item) for item in data]
    else:
        return data
