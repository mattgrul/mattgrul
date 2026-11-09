import json
import unittest
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

from card import THEMES, stats, svg, uptime


def calendar(counts, end=date(2026, 11, 9)):
    return [{"date": (end - timedelta(days=len(counts) - 1 - i)).isoformat(), "contributionCount": n}
            for i, n in enumerate(counts)]


class StreakTest(unittest.TestCase):
    def test_a_quiet_today_keeps_the_streak(self):
        self.assertEqual(stats(calendar([0, 3, 1, 0]))["current"], 2)

    def test_a_quiet_yesterday_ends_the_streak(self):
        self.assertEqual(stats(calendar([4, 0, 2]))["current"], 1)


class UptimeTest(unittest.TestCase):
    def test_borrows_the_days_of_the_month_before(self):
        self.assertEqual(uptime(date(2018, 6, 17), date(2026, 11, 9)), "8 Years, 4 Months, 23 Days")


class CardTest(unittest.TestCase):
    def test_both_cards_are_well_formed_xml(self):
        picture = json.loads((Path(__file__).parent / "portrait.json").read_text())
        days = calendar([i % 5 for i in range(365)])
        for theme in THEMES:
            ET.fromstring(svg(theme, picture, days, date(2026, 11, 9)))


if __name__ == "__main__":
    unittest.main()
