"""
Sunrise to Sunset Chart - Calculator Module
Handles astronomical calculations for sunrise and sunset times.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional
from astral import LocationInfo
from astral.sun import sun
import logging

logger = logging.getLogger(__name__)


class SunCalculator:
    """Calculates sunrise and sunset times for a given location."""

    def __init__(self, latitude: float, longitude: float, timezone: str = "UTC"):
        """
        Initialize the sun calculator.

        Args:
            latitude: Latitude of the location in degrees
            longitude: Longitude of the location in degrees
            timezone: Timezone string (e.g., "America/New_York")
        """
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.location = LocationInfo(
            latitude=latitude,
            longitude=longitude,
            timezone=timezone
        )

    def calculate_year(self, year: Optional[int] = None) -> Tuple[List[date], List[float], List[float], List[float]]:
        """
        Calculate sunrise, noon, and sunset times for every day of the year.

        Args:
            year: Year to calculate for (defaults to current year)

        Returns:
            Tuple of (dates, sunrise_times, noon_times, sunset_times)
            - dates: List of date objects
            - sunrise_times: List of sunrise times as hours (0-24)
            - noon_times: List of solar noon times as hours (0-24)
            - sunset_times: List of sunset times as hours (0-24)
        """
        if year is None:
            year = datetime.now().year

        dates = []
        sunrise_times = []
        noon_times = []
        sunset_times = []

        # Calculate for all days in the year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)

        current_date = start_date
        while current_date <= end_date:
            try:
                s = sun(self.location.observer, date=current_date, tzinfo=self.timezone)

                sunrise = s['sunrise']
                noon = s['noon']  # Solar noon (sun at highest point/zenith)
                sunset = s['sunset']

                # Convert to decimal hours for plotting
                sunrise_hour = sunrise.hour + sunrise.minute / 60.0 + sunrise.second / 3600.0
                noon_hour = noon.hour + noon.minute / 60.0 + noon.second / 3600.0
                sunset_hour = sunset.hour + sunset.minute / 60.0 + sunset.second / 3600.0

                dates.append(current_date)
                sunrise_times.append(sunrise_hour)
                noon_times.append(noon_hour)
                sunset_times.append(sunset_hour)

            except ValueError as e:
                # Handle polar regions where sun may not rise/set
                logger.warning(f"Cannot calculate sun times for {current_date}: {e}")
                # Use None or special values for days without sunrise/sunset
                dates.append(current_date)
                sunrise_times.append(None)
                noon_times.append(None)
                sunset_times.append(None)

            current_date += timedelta(days=1)

        return dates, sunrise_times, noon_times, sunset_times

    def calculate_day(self, target_date: date) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Calculate sunrise and sunset for a specific day.

        Args:
            target_date: Date to calculate for

        Returns:
            Tuple of (sunrise, sunset) as datetime objects, or None if cannot calculate
        """
        try:
            s = sun(self.location.observer, date=target_date, tzinfo=self.timezone)
            return s['sunrise'], s['sunset']
        except ValueError as e:
            logger.warning(f"Cannot calculate sun times for {target_date}: {e}")
            return None, None


def get_sun_times(latitude: float, longitude: float, timezone: str = "UTC",
                  year: Optional[int] = None) -> Tuple[List[date], List[float], List[float], List[float]]:
    """
    Convenience function to get sun times for a location.

    Args:
        latitude: Latitude in degrees
        longitude: Longitude in degrees
        timezone: Timezone string
        year: Year to calculate for (defaults to current year)

    Returns:
        Tuple of (dates, sunrise_times, noon_times, sunset_times)
    """
    calculator = SunCalculator(latitude, longitude, timezone)
    return calculator.calculate_year(year)
