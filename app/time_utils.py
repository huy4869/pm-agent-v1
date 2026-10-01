from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone, tzinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def app_timezone() -> tzinfo:
    name = os.getenv("PM_TIMEZONE", "Asia/Ho_Chi_Minh")
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        # Windows Python may not ship an IANA database. requirements.txt also
        # includes tzdata, but keep a safe ICT fallback so dashboard analysis
        # never fails just because timezone data is absent.
        if name == "Asia/Ho_Chi_Minh":
            return timezone(timedelta(hours=7), name="ICT")
        return timezone.utc


def local_now(now: datetime | None = None) -> datetime:
    if now is None:
        now = datetime.now(timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now.astimezone(app_timezone())


def local_today(now: datetime | None = None) -> date:
    return local_now(now).date()


def days_until(value: str | None, now: datetime | None = None) -> int | None:
    if not value:
        return None
    return (date.fromisoformat(value) - local_today(now)).days
