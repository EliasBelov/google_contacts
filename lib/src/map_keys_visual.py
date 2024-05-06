def map_keys_visual(d, parent_key='', path_list=None):
    """
    Рекурсивно обходит словарь и возвращает визуализацию структуры словаря.

    Args:
    - d (dict or list): Словарь или список для обхода.
    - parent_key (str, optional): Родительский ключ для текущей итерации. По умолчанию пустая строка.
    - path_list (list, optional): Список для сохранения текущих путей. По умолчанию None.

    Returns:
    - list: Список визуализированных путей до каждого ключа.
    """

    if path_list is None:
        path_list = []

    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key} → {k}" if parent_key else k
            path_list.append(new_key)

            if isinstance(v, (dict, list)):
                map_keys_visual(v, new_key, path_list)

    elif isinstance(d, list):
        for idx, item in enumerate(d):
            new_key = f"{parent_key} → [{idx}]"
            path_list.append(new_key)

            if isinstance(item, (dict, list)):
                map_keys_visual(item, new_key, path_list)

    return path_list