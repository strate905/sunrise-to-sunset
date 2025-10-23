"""
Tests for the utils module.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import pytest
from src.utils import format_time, validate_coordinates, setup_logging
from src.geocoder import LocationData


class TestFormatTime:
    """Test cases for time formatting."""

    def test_format_time_whole_hours(self):
        """Test formatting whole hours."""
        assert format_time(0.0) == "00:00"
        assert format_time(12.0) == "12:00"
        assert format_time(23.0) == "23:00"

    def test_format_time_with_minutes(self):
        """Test formatting times with minutes."""
        assert format_time(7.5) == "07:30"
        assert format_time(16.75) == "16:45"
        assert format_time(9.25) == "09:15"

    def test_format_time_edge_cases(self):
        """Test edge cases."""
        assert format_time(0.0) == "00:00"
        assert format_time(24.0) == "24:00"
        assert format_time(23.99) == "23:59"


class TestValidateCoordinates:
    """Test cases for coordinate validation."""

    def test_validate_valid_coordinates(self):
        """Test validation of valid coordinates."""
        assert validate_coordinates(0.0, 0.0) is True
        assert validate_coordinates(51.5074, -0.1278) is True
        assert validate_coordinates(-90.0, -180.0) is True
        assert validate_coordinates(90.0, 180.0) is True

    def test_validate_invalid_latitude(self):
        """Test validation of invalid latitude."""
        assert validate_coordinates(91.0, 0.0) is False
        assert validate_coordinates(-91.0, 0.0) is False
        assert validate_coordinates(100.0, 0.0) is False

    def test_validate_invalid_longitude(self):
        """Test validation of invalid longitude."""
        assert validate_coordinates(0.0, 181.0) is False
        assert validate_coordinates(0.0, -181.0) is False
        assert validate_coordinates(0.0, 200.0) is False

    def test_validate_both_invalid(self):
        """Test validation when both coordinates are invalid."""
        assert validate_coordinates(91.0, 181.0) is False
        assert validate_coordinates(-100.0, -200.0) is False


class TestSetupLogging:
    """Test cases for logging setup."""

    def test_setup_logging(self):
        """Test that logging setup doesn't raise errors."""
        # Just verify it doesn't crash
        setup_logging()

    def test_setup_logging_with_level(self):
        """Test logging setup with custom level."""
        import logging
        setup_logging(level=logging.DEBUG)
        # Verify it doesn't crash with custom level
