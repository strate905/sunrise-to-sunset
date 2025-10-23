"""
Sunrise to Sunset Chart - Geocoder Module
Handles location resolution from city names or coordinates.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from typing import List, Tuple, Optional, Dict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder
import logging

logger = logging.getLogger(__name__)


def _extract_local_names(name_details: Optional[Dict[str, str]]) -> Dict[str, str]:
    """
    Pull language-keyed names from Nominatim namedetails payload.

    Args:
        name_details: Raw namedetails dictionary from Nominatim.

    Returns:
        Dictionary keyed by ISO language code.
    """
    if not name_details:
        return {}

    localized: Dict[str, str] = {}
    for key, value in name_details.items():
        if not value:
            continue
        if key == "name":
            # Store raw name under 'default' when provided.
            localized.setdefault("default", value)
            continue
        if key.startswith("name:"):
            lang_code = key.split(":", 1)[1].lower()
            localized[lang_code] = value
    return localized


class LocationData:
    """Represents a geographic location with all necessary data."""

    def __init__(
        self,
        name: str,
        latitude: float,
        longitude: float,
        timezone: str,
        country: Optional[str] = None,
        state: Optional[str] = None,
        local_names: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize location data.

        Args:
            name: Location name
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            timezone: Timezone string (e.g., "America/New_York")
            country: Country name (optional)
            state: State/region name (optional)
            local_names: Mapping of ISO language codes to localized names
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.country = country
        self.state = state
        self.local_names: Dict[str, str] = local_names or {}

    def __str__(self) -> str:
        """Return a string representation of the location."""
        parts = [self.name]
        if self.state:
            parts.append(self.state)
        if self.country:
            parts.append(self.country)
        return ", ".join(parts)

    def __repr__(self) -> str:
        """Return a detailed representation of the location."""
        return (
            "LocationData("
            f"name='{self.name}', lat={self.latitude}, lon={self.longitude}, "
            f"tz='{self.timezone}', locales={list(self.local_names.keys())}"
            ")"
        )

    def get_localized_name(self, language: str) -> str:
        """
        Return a localized place name for the requested language.

        Args:
            language: Either an ISO language code (e.g., 'en', 'ar', 'ja')
                      or a human-readable language key ('english', 'arabic', 'japanese')

        Returns:
            Localized name if available; otherwise the default name.
        """
        if not language:
            return self.name

        # Accept common aliases so callers can pass human-readable values.
        language_aliases = {
            "english": "en",
            "arabic": "ar",
            "japanese": "ja",
        }
        lookup_key = language_aliases.get(language.lower(), language.lower())
        return self.local_names.get(lookup_key, self.name)


class GeocoderService:
    """Service for geocoding city names and resolving locations."""

    def __init__(self, user_agent: str = "sunrise-to-sunset-chart"):
        """
        Initialize the geocoder service.

        Args:
            user_agent: User agent string for the geocoding service
        """
        self.geolocator = Nominatim(user_agent=user_agent)
        self.tz_finder = TimezoneFinder()

    def parse_coordinates(self, input_str: str) -> Optional[Tuple[float, float]]:
        """
        Parse coordinate string in format "lat, lon".

        Args:
            input_str: String containing coordinates

        Returns:
            Tuple of (latitude, longitude) or None if invalid
        """
        try:
            parts = input_str.split(',')
            if len(parts) == 2:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())

                # Validate ranges
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    return lat, lon
        except (ValueError, AttributeError):
            pass

        return None

    def get_timezone(self, latitude: float, longitude: float) -> str:
        """
        Get timezone for given coordinates.

        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees

        Returns:
            Timezone string (defaults to "UTC" if not found)
        """
        try:
            tz = self.tz_finder.timezone_at(lat=latitude, lng=longitude)
            return tz if tz else "UTC"
        except Exception as e:
            logger.warning(f"Could not determine timezone: {e}")
            return "UTC"

    def geocode_city(self, city_name: str, limit: int = 10) -> List[LocationData]:
        """
        Geocode a city name and return possible matches.

        Args:
            city_name: Name of the city to search for
            limit: Maximum number of results to return

        Returns:
            List of LocationData objects for matching locations
        """
        try:
            # Search for the city
            locations = self.geolocator.geocode(
                city_name,
                exactly_one=False,
                limit=limit,
                addressdetails=True,
                namedetails=True
            )

            if not locations:
                return []

            results = []
            for loc in locations:
                # Extract address details
                raw = loc.raw or {}
                address = raw.get('address', {})
                name_details = raw.get('namedetails', {})
                name = (address.get('city') or
                        address.get('town') or
                        address.get('village') or
                        address.get('municipality') or
                        loc.address.split(',')[0])

                country = address.get('country')
                state = address.get('state')

                # Get timezone
                timezone = self.get_timezone(loc.latitude, loc.longitude)

                location_data = LocationData(
                    name=name,
                    latitude=loc.latitude,
                    longitude=loc.longitude,
                    timezone=timezone,
                    country=country,
                    state=state,
                    local_names=_extract_local_names(name_details)
                )
                results.append(location_data)

            return results

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Geocoding error: {e}")
            return []

    def get_location_from_coordinates(self, latitude: float, longitude: float) -> LocationData:
        """
        Create location data from coordinates.

        Args:
            latitude: Latitude in degrees
            longitude: Longitude in degrees

        Returns:
            LocationData object
        """
        timezone = self.get_timezone(latitude, longitude)

        # Try to get a name for the coordinates via reverse geocoding
        try:
            location = self.geolocator.reverse(
                f"{latitude}, {longitude}",
                addressdetails=True,
                namedetails=True
            )
            if location:
                raw = location.raw or {}
                address = raw.get('address', {})
                name_details = raw.get('namedetails', {})
                name = (address.get('city') or
                        address.get('town') or
                        address.get('village') or
                        address.get('municipality') or
                        f"Location {latitude:.2f}, {longitude:.2f}")
                country = address.get('country')
                state = address.get('state')
            else:
                name = f"Location {latitude:.2f}, {longitude:.2f}"
                country = None
                state = None
                name_details = {}
        except Exception as e:
            logger.warning(f"Reverse geocoding failed: {e}")
            name = f"Location {latitude:.2f}, {longitude:.2f}"
            country = None
            state = None
            name_details = {}

        return LocationData(
            name=name,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            country=country,
            state=state,
            local_names=_extract_local_names(name_details)
        )

    def resolve_location(self, user_input: str) -> Tuple[Optional[LocationData], List[LocationData]]:
        """
        Resolve a location from user input (city name or coordinates).

        Args:
            user_input: User input string

        Returns:
            Tuple of (selected_location, all_matches)
            - If coordinates provided: (location, [])
            - If single match: (location, [])
            - If multiple matches: (None, [list of matches])
            - If no match: (None, [])
        """
        # Try to parse as coordinates first
        coords = self.parse_coordinates(user_input)
        if coords:
            location = self.get_location_from_coordinates(coords[0], coords[1])
            return location, []

        # Otherwise, geocode as city name
        matches = self.geocode_city(user_input)

        if len(matches) == 0:
            return None, []
        elif len(matches) == 1:
            return matches[0], []
        else:
            return None, matches
