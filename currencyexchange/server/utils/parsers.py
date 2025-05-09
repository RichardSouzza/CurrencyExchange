from datetime import date, datetime


def parse_date_to_datetime(dt: date) -> datetime:
    if isinstance(dt, str):
        return datetime.strptime(dt, "%Y-%m-%d")
    elif isinstance(dt, date):
        return datetime(dt.year, dt.month, dt.day)
    elif isinstance(dt, datetime):
        return dt
    else:
        raise ValueError("Invalid date format")
