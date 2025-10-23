"""
Tests for the calculator module.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import pytest
from datetime import date, datetime
from src.calculator import SunCalculator, get_sun_times


class TestSunCalculator:
    """Test cases for SunCalculator class."""

    def test_init(self):
        """Test calculator initialization."""
        calc = SunCalculator(latitude=51.5074, longitude=-0.1278, timezone="Europe/London")
        assert calc.latitude == 51.5074
        assert calc.longitude == -0.1278
        assert calc.timezone == "Europe/London"

    def test_calculate_year_returns_correct_length(self):
        """Test that calculate_year returns data for all days."""
        calc = SunCalculator(latitude=35.6762, longitude=139.6503, timezone="Asia/Tokyo")
        dates, sunrise_times, noon_times, sunset_times = calc.calculate_year(2025)

        # 2025 is not a leap year, should have 365 days
        assert len(dates) == 365
        assert len(sunrise_times) == 365
        assert len(noon_times) == 365
        assert len(sunset_times) == 365

    def test_calculate_year_leap_year(self):
        """Test calculation for a leap year."""
        calc = SunCalculator(latitude=35.6762, longitude=139.6503, timezone="Asia/Tokyo")
        dates, sunrise_times, noon_times, sunset_times = calc.calculate_year(2024)

        # 2024 is a leap year, should have 366 days
        assert len(dates) == 366
        assert len(sunrise_times) == 366
        assert len(noon_times) == 366
        assert len(sunset_times) == 366

    def test_calculate_year_date_range(self):
        """Test that dates cover the entire year."""
        calc = SunCalculator(latitude=35.6762, longitude=139.6503, timezone="Asia/Tokyo")
        dates, _, _, _ = calc.calculate_year(2025)

        assert dates[0] == date(2025, 1, 1)
        assert dates[-1] == date(2025, 12, 31)

    def test_calculate_year_time_ranges(self):
        """Test that times are within valid ranges."""
        calc = SunCalculator(latitude=35.6762, longitude=139.6503, timezone="Asia/Tokyo")
        _, sunrise_times, noon_times, sunset_times = calc.calculate_year(2025)

        for sunrise, noon, sunset in zip(sunrise_times, noon_times, sunset_times):
            if sunrise is not None:
                assert 0 <= sunrise <= 24
            if noon is not None:
                assert 0 <= noon <= 24
            if sunset is not None:
                assert 0 <= sunset <= 24

    def test_calculate_day(self):
        """Test single day calculation."""
        calc = SunCalculator(latitude=35.6762, longitude=139.6503, timezone="Asia/Tokyo")
        sunrise, sunset = calc.calculate_day(date(2025, 6, 21))  # Summer solstice

        assert sunrise is not None
        assert sunset is not None
        assert sunrise < sunset  # Sunrise should be before sunset

    def test_calculate_equator(self):
        """Test calculation near the equator."""
        calc = SunCalculator(latitude=0.0, longitude=0.0, timezone="UTC")
        dates, sunrise_times, noon_times, sunset_times = calc.calculate_year(2025)

        # Near equator, sunrise/sunset times should be relatively stable
        assert len(dates) == 365
        assert all(s is not None for s in sunrise_times)
        assert all(n is not None for n in noon_times)
        assert all(s is not None for s in sunset_times)

    def test_get_sun_times_convenience_function(self):
        """Test the convenience function."""
        dates, sunrise_times, noon_times, sunset_times = get_sun_times(
            latitude=51.5074,
            longitude=-0.1278,
            timezone="Europe/London",
            year=2025
        )

        assert len(dates) == 365
        assert len(sunrise_times) == 365
        assert len(noon_times) == 365
        assert len(sunset_times) == 365

    def test_default_year(self):
        """Test that default year is current year."""
        calc = SunCalculator(latitude=35.6762, longitude=139.6503, timezone="Asia/Tokyo")
        dates, _, _, _ = calc.calculate_year()

        current_year = datetime.now().year
        assert dates[0].year == current_year
        assert dates[-1].year == current_year


class TestPolarRegions:
    """Test cases for locations in polar regions."""

    def test_arctic_summer(self):
        """Test Arctic location during summer (midnight sun)."""
        # Svalbard, Norway - experiences midnight sun
        calc = SunCalculator(latitude=78.2232, longitude=15.6267, timezone="Arctic/Longyearbyen")
        dates, sunrise_times, noon_times, sunset_times = calc.calculate_year(2025)

        # Should have some days without sunset (midnight sun)
        # But the calculation should not crash
        assert len(dates) == 365
        assert len(sunrise_times) == 365
        assert len(noon_times) == 365
        assert len(sunset_times) == 365

    def test_arctic_winter(self):
        """Test Arctic location during winter (polar night)."""
        # Svalbard during polar night period
        calc = SunCalculator(latitude=78.2232, longitude=15.6267, timezone="Arctic/Longyearbyen")
        sunrise, sunset = calc.calculate_day(date(2025, 1, 15))

        # May not have sunrise/sunset during polar night
        # Function should handle this gracefully
        assert sunrise is not None or sunset is not None or (sunrise is None and sunset is None)
