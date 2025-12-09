from datetime import datetime, timedelta


def wib_now() -> datetime:
    """Return current time in WIB (UTC+7), naive datetime."""
    return datetime.utcnow() + timedelta(hours=7)


def wib_day_range(ref: datetime | None = None):
    """Return UTC-naive start and end datetimes for the WIB day of `ref`.

    If `ref` is None, use current WIB time.
    """
    now_wib = ref or wib_now()
    start_wib = datetime(now_wib.year, now_wib.month, now_wib.day)
    end_wib = start_wib + timedelta(days=1)
    # Convert WIB day range to UTC-naive range (subtract 7 hours)
    start_utc = start_wib - timedelta(hours=7)
    end_utc = end_wib - timedelta(hours=7)
    return start_utc, end_utc