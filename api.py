def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return 'en el futuro :O'

    if day_diff == 0:
        if second_diff < 10:
            return "justo ahora"
        if second_diff < 60:
            return "hace " + str(second_diff) + " segundos"
        if second_diff < 120:
            return "hace un minuto"
        if second_diff < 3600:
            return "hace " + str(int(second_diff / 60)) + " minutos"
        if second_diff < 7200:
            return "hace una hora"
        if second_diff < 86400:
            return "hace " + str(int(second_diff / 3600)) + " horas"
    if day_diff == 1:
        return "ayer"
    if day_diff < 7:
        return "hace " + str(day_diff) + " días"
    if day_diff < 31:
        return "hace " + str(day_diff / 7) + " semanas"
    if day_diff < 365:
        return "hace " + str(day_diff / 30) + " meses"
    return "hace " + str(day_diff / 365) + " años"
