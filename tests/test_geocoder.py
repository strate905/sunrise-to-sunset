"""
Tests for the geocoder module.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import pytest
from src.geocoder import LocationData, GeocoderService


class TestLocationData:
    """Test cases for LocationData class."""

    def test_init(self):
        """Test LocationData initialization."""
        loc = LocationData(
            name="London",
            latitude=51.5074,
            longitude=-0.1278,
            timezone="Europe/London",
            country="United Kingdom"
        )

        assert loc.name == "London"
        assert loc.latitude == 51.5074
        assert loc.longitude == -0.1278
        assert loc.timezone == "Europe/London"
        assert loc.country == "United Kingdom"
        assert loc.local_names == {}

    def test_str_with_country(self):
        """Test string representation with country."""
        loc = LocationData(
            name="Paris",
            latitude=48.8566,
            longitude=2.3522,
            timezone="Europe/Paris",
            country="France"
        )

        assert "Paris" in str(loc)
        assert "France" in str(loc)

    def test_str_with_state_and_country(self):
        """Test string representation with state and country."""
        loc = LocationData(
            name="Austin",
            latitude=30.2672,
            longitude=-97.7431,
            timezone="America/Chicago",
            country="United States",
            state="Texas"
        )

        assert "Austin" in str(loc)
        assert "Texas" in str(loc)
        assert "United States" in str(loc)

    def test_repr(self):
        """Test repr representation."""
        loc = LocationData(
            name="Tokyo",
            latitude=35.6762,
            longitude=139.6503,
            timezone="Asia/Tokyo"
        )

        repr_str = repr(loc)
        assert "LocationData" in repr_str
        assert "Tokyo" in repr_str
        assert "locales" in repr_str

    def test_get_localized_name(self):
        """Localized names fallback to defaults when missing."""
        loc = LocationData(
            name="Munich",
            latitude=48.1351,
            longitude=11.5820,
            timezone="Europe/Berlin",
            local_names={"en": "Munich", "de": "München", "ja": "ミュンヘン"}
        )

        assert loc.get_localized_name("english") == "Munich"
        assert loc.get_localized_name("en") == "Munich"
        assert loc.get_localized_name("de") == "München"
        assert loc.get_localized_name("japanese") == "ミュンヘン"
        assert loc.get_localized_name("fr") == "Munich"


class TestGeocoderService:
    """Test cases for GeocoderService class."""

    def test_init(self):
        """Test GeocoderService initialization."""
        service = GeocoderService()
        assert service.geolocator is not None
        assert service.tz_finder is not None

    def test_parse_coordinates_valid(self):
        """Test parsing valid coordinates."""
        service = GeocoderService()

        coords = service.parse_coordinates("51.5074, -0.1278")
        assert coords is not None
        assert coords[0] == pytest.approx(51.5074, rel=1e-4)
        assert coords[1] == pytest.approx(-0.1278, rel=1e-4)

    def test_parse_coordinates_with_spaces(self):
        """Test parsing coordinates with extra spaces."""
        service = GeocoderService()

        coords = service.parse_coordinates("  40.7128  ,  -74.0060  ")
        assert coords is not None
        assert coords[0] == pytest.approx(40.7128, rel=1e-4)
        assert coords[1] == pytest.approx(-74.0060, rel=1e-4)

    def test_parse_coordinates_invalid_format(self):
        """Test parsing invalid coordinate format."""
        service = GeocoderService()

        assert service.parse_coordinates("not coordinates") is None
        assert service.parse_coordinates("51.5074") is None
        assert service.parse_coordinates("51.5074, ") is None

    def test_parse_coordinates_out_of_range(self):
        """Test parsing out-of-range coordinates."""
        service = GeocoderService()

        assert service.parse_coordinates("91.0, 0.0") is None  # Latitude > 90
        assert service.parse_coordinates("-91.0, 0.0") is None  # Latitude < -90
        assert service.parse_coordinates("0.0, 181.0") is None  # Longitude > 180
        assert service.parse_coordinates("0.0, -181.0") is None  # Longitude < -180

    def test_get_timezone_valid(self):
        """Test getting timezone for valid coordinates."""
        service = GeocoderService()

        # London
        tz = service.get_timezone(51.5074, -0.1278)
        assert tz == "Europe/London"

        # New York
        tz = service.get_timezone(40.7128, -74.0060)
        assert tz == "America/New_York"

    def test_get_timezone_ocean(self):
        """Test getting timezone for ocean coordinates."""
        service = GeocoderService()

        # Middle of Atlantic Ocean
        tz = service.get_timezone(0.0, -30.0)
        # Should return a valid timezone (UTC or Etc/GMT variant)
        assert tz is not None
        assert "GMT" in tz or tz == "UTC"

    @pytest.mark.skip(reason="Requires network connection and may be slow")
    def test_geocode_city_single_result(self):
        """Test geocoding a city with unique name."""
        service = GeocoderService()

        results = service.geocode_city("Reykjavik")
        assert len(results) > 0
        assert "Reykjavik" in results[0].name or "Reykjavík" in results[0].name

    @pytest.mark.skip(reason="Requires network connection and may be slow")
    def test_geocode_city_multiple_results(self):
        """Test geocoding a city with multiple matches."""
        service = GeocoderService()

        results = service.geocode_city("Springfield")
        assert len(results) > 1  # Many Springfields exist

    @pytest.mark.skip(reason="Requires network connection and may be slow")
    def test_geocode_city_not_found(self):
        """Test geocoding a non-existent city."""
        service = GeocoderService()

        results = service.geocode_city("Nonexistentville123456")
        assert len(results) == 0

    def test_get_location_from_coordinates(self):
        """Test creating location from coordinates."""
        service = GeocoderService()

        loc = service.get_location_from_coordinates(51.5074, -0.1278)
        assert loc is not None
        assert loc.latitude == 51.5074
        assert loc.longitude == -0.1278
        assert loc.timezone is not None

    def test_resolve_location_with_coordinates(self):
        """Test resolving location from coordinate string."""
        service = GeocoderService()

        location, matches = service.resolve_location("40.7128, -74.0060")
        assert location is not None
        assert len(matches) == 0  # No ambiguity with coordinates
        assert location.latitude == pytest.approx(40.7128, rel=1e-4)
        assert location.longitude == pytest.approx(-74.0060, rel=1e-4)

    @pytest.mark.skip(reason="Requires network connection and may be slow")
    def test_resolve_location_with_city_name(self):
        """Test resolving location from city name."""
        service = GeocoderService()

        location, matches = service.resolve_location("London")
        # Should return either a single location or multiple matches
        assert location is not None or len(matches) > 0
