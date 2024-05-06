def count_groups(data, group_value):
    """
        Подсчет групп внутри словаря
    """
    count = 0
    for entry in data.values():
        for item in entry:
            if 'group' in item and item['group'] == group_value:
                count += 1
    return count

def count_drivers(data, driverName, groupName):
    count = 0
    for _, value in data.items():
        for entry in value:
            if entry.get('group') == groupName and entry.get('driverName') == driverName:
                count += 1
    return count