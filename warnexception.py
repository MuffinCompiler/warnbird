
def safe_read_cast(cfg_dict, section, item, to_type, default=None):

    if section not in cfg_dict:
        print(f"Expected key {section} in dict {cfg_dict}. Using default value for {section}.{item} = {default}")
        return default
        # TODO Logging interface
    if item not in cfg_dict[section]:
        print(f"Expected item {item} in section {section} in dict {cfg_dict}. Using default value for {section}.{item} = {default}")
        return default

    item_data = cfg_dict[section][item]

    try:
        return to_type(item_data)
    except (ValueError, TypeError):
        print(f"Can't convert {section}.{item} to {to_type}. Using default = {default}")
        return default

