from datetime import datetime

def yearDecider(date:int,month:int) -> int:

    today = datetime.now()
    currentYear = today.year
    currentTimestamp = today.timestamp()

    targetTimestamp = datetime(
        currentYear,
        month,
        date,
        23,59,59
    ).timestamp()

    if targetTimestamp <= currentTimestamp:
        return currentYear + 1
    else :
        return currentYear