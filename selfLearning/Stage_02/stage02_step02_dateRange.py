from datetime import datetime, timedelta

def get_date_range(time_range: int) -> tuple[str, str]:
    """
    Fetch start and end date of dates in `range`, which are in format of YYYYMMDD.
    :param time_range: time range.
    :return: a tuple of (start date, end date).
    """
    raw_end_date = datetime.today()
    raw_start_date = raw_end_date - timedelta(days=time_range)

    starting_date = raw_start_date.strftime("%Y%m%d")
    ending_date = raw_end_date.strftime("%Y%m%d")

    return starting_date, ending_date

if __name__ == "__main__":
    start_date, end_date = get_date_range(365)
    print("start date is: ", start_date)
    print("end date is: ", end_date)