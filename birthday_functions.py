from datetime import timedelta, date


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


def get_upcoming_birthdays(records, days: int = 7):
    upcoming_birthdays = []
    today = date.today()

    for record in records:
        if record.birthday is None:
            continue

        birthday_this_year = record.birthday.value.replace(year=today.year).date()

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        if 0 <= (birthday_this_year - today).days <= days:
            if birthday_this_year.weekday() in (5, 6):
                birthday_this_year = adjust_for_weekend(birthday_this_year)

            congratulation_date_str = birthday_this_year.strftime('%d.%m.%Y')

            upcoming_birthdays.append({
                "name": record.name.value,
                "birthday": congratulation_date_str})
    return upcoming_birthdays
