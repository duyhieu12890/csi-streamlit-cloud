import datetime

non_special = {
    "1": 31,
    "2": 28,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31
}

special = {
    "1": 31,
    "2": 29,
    "3": 31,
    "4": 30,
    "5": 31,
    "6": 30,
    "7": 31,
    "8": 31,
    "9": 30,
    "10": 31,
    "11": 30,
    "12": 31
}

# Hàm kiểm tra năm nhuận (không dùng thư viện datetime)
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False

def dayinmonth(year: int, month:int) -> int:
    if is_leap_year(year):
        return special[str(month)]
    else:
        return non_special[str(month)]

def build_range(begin:str, end:str, data:dict, default_none=0):
    start_date = datetime.date.fromisoformat(begin)
    end_date = datetime.date.fromisoformat(end)
    result = []

    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        day = current_date.day

        year_str = str(year)
        month_str = str(month)
        day_str = str(day)

        if data.get(year_str) and data[year_str].get(month_str) and data[year_str][month_str].get(day_str) is not None:
            result.append(data[year_str][month_str][day_str])
        else:
            result.append(default_none)

        current_date += datetime.timedelta(days=1)

    return result

def calculate_range(begin: str, end: str) -> int:
    """
    Tính số ngày từ ngày bắt đầu đến ngày kết thúc (bao gồm cả ngày bắt đầu và ngày kết thúc).

    Args:
        begin: Ngày bắt đầu ở định dạng ISO 8601 (ví dụ: "2023-10-26").
        end: Ngày kết thúc ở định dạng ISO 8601 (ví dụ: "2023-10-31").

    Returns:
        Số ngày trong khoảng thời gian.
    """
    start_date = datetime.date.fromisoformat(begin)
    end_date = datetime.date.fromisoformat(end)

    delta = end_date - start_date
    return delta.days + 1  # Cộng 1 để bao gồm cả ngày bắt đầu và ngày kết thúc

def calulate_begin_from_end(end: str, days):
    """
    Tính ngày bắt đầu từ ngày kết thúc và số ngày.

    Args:
        end: Ngày kết thúc ở định dạng ISO 8601 (ví dụ: "2023-10-31").
        days: Số ngày cần tính lùi lại.

    Returns:
        Ngày bắt đầu ở định dạng ISO 8601.
    """
    end_date = datetime.date.fromisoformat(end)
    begin_date = end_date - datetime.timedelta(days=days - 1)  # Cộng 1 để bao gồm cả ngày kết thúc
    return begin_date.isoformat()

def build_list_date(begin: str, end: str):
    start_date = datetime.date.fromisoformat(begin)
    end_date = datetime.date.fromisoformat(end)
    result = []

    for n in range((end_date - start_date).days + 1):
        current_date = start_date + datetime.timedelta(n)
        result.append(current_date.isoformat())

    return result


data = {
    "2025": {
        "7": {
            "7": 67,
            "8": 67.5,
            "9": 68,
            "10": 68,
            "11": 68,
            "12": 68.5
        }
    }
}
