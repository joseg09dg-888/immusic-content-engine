import pytest, sys
from datetime import datetime, timezone, timedelta
sys.path.insert(0, "src")
from core.scheduler import ContentScheduler, COT

def make_sched():
    return ContentScheduler.__new__(ContentScheduler)

def test_monday_publish():
    s = make_sched()
    assert s.is_publish_day(datetime(2026, 6, 1, 18, 0, tzinfo=COT)) is True

def test_tuesday_no_publish():
    s = make_sched()
    assert s.is_publish_day(datetime(2026, 6, 2, 18, 0, tzinfo=COT)) is False

def test_wednesday_publish():
    s = make_sched()
    assert s.is_publish_day(datetime(2026, 6, 3, 18, 0, tzinfo=COT)) is True

def test_friday_publish():
    s = make_sched()
    assert s.is_publish_day(datetime(2026, 6, 5, 18, 0, tzinfo=COT)) is True

def test_saturday_no_publish():
    s = make_sched()
    assert s.is_publish_day(datetime(2026, 6, 6, 18, 0, tzinfo=COT)) is False

def test_sunday_no_publish():
    s = make_sched()
    assert s.is_publish_day(datetime(2026, 6, 7, 18, 0, tzinfo=COT)) is False
