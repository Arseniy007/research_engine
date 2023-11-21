from typing import Literal


FORMATS = Literal["apa", "mla"]
INTERNET_BIRTHDAY = 1969
MONTHS = {"01": "January", "02": "February", "03": "March", "04": "April", 
            "05": "May", "06": "June", "07": "July", "08": "August", 
            "09": "September", "10": "October", "11": "November", "12": "December"}


def validate_date(date: str) -> bool:
    """Check given date (should be: 1937-02-02)"""
    try:
        year, month, day = date.split("-")
    except IndexError:
        return False
    else:
        try:
            year_num, month_num, day_num = int(year), int(month), int(day)
        except ValueError:
            return False

    if len(year) != 4:
        return False
    elif int(year[0]) > 2:
        return False
    elif year_num < INTERNET_BIRTHDAY:
        return False
    elif len(month) != 2:
        return False
    elif month_num < 1 or month_num > 12:
        return False
    elif len(day) != 2:
        return False
    if day_num < 1 or day_num > 31:
        return False
    else:
        return True
    

def format_date(date: str, format_: FORMATS):
    """Turns 2001-01-01 into '2001, January 1'"""
    year, month, day = date.split("-")

    # Turn month from num to word
    month = MONTHS[month]

    # Delete '0' from day
    if day[0] == "0":
        day = day[-1]

    if format_ == "apa":
        return f"{year}, {month} {day}"
    elif format_ == "mla":
        return f"{day} {month} {year}"
    else:
        return None
