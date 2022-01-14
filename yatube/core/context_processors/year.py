import datetime as dt


def year(request):
    """Добавляет переменную с текущим годом."""
    today = dt.date.today()
    year = today.year
    return {
        'year': year
    }
