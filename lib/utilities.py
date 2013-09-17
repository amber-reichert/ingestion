# Utility methods 

def iterify(iterable):
    """Treat iterating over a single item or an iterator seamlessly"""
    if (isinstance(iterable, basestring) or isinstance(iterable, dict)):
        iterable = [iterable]
    try:
        iter(iterable)
    except TypeError:
        iterable = [iterable]

    return iterable

def remove_key_prefix(data, prefix):
    """Removes the prefix from keys in a dictionary"""
    for key in data.keys():
        if not key == "originalRecord":
            new_key = key.replace(prefix, "")
            if new_key != key:
                data[new_key] = data[key]
                del data[key]
            for item in iterify(data[new_key]):
                if isinstance(item, dict):
                    remove_key_prefix(item, prefix)

    return data
