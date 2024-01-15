from typing import Literal


FORMATS = Literal["apa", "mla"]
MONTHS = {"01": "January", "02": "February", "03": "March", "04": "April", 
            "05": "May", "06": "June", "07": "July", "08": "August", 
            "09": "September", "10": "October", "11": "November", "12": "December"}


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
