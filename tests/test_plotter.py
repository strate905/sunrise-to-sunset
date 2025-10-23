"""
Tests for the plotter module.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import pytest
from datetime import date
import os
from src.plotter import SunChart, plot_sun_times


class TestSunChart:
    """Test cases for SunChart class."""

    def test_init(self):
        """Test SunChart initialization."""
        chart = SunChart(figsize=(12, 6), dpi=100)
        assert chart.figsize == (12, 6)
        assert chart.dpi == 100

    def test_init_defaults(self):
        """Test SunChart initialization with defaults."""
        chart = SunChart()
        assert chart.figsize == (14, 8)
        assert chart.dpi == 100

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        chart = SunChart()

        # Test with special characters
        assert chart._sanitize_filename("London, UK") == "London__UK"
        assert chart._sanitize_filename("New York") == "New_York"
        assert chart._sanitize_filename("Test:Test") == "Test_Test"
        assert chart._sanitize_filename("Test/Test") == "Test_Test"
        assert chart._sanitize_filename("Test<>Test") == "Test__Test"

    def test_sanitize_filename_multiple_spaces(self):
        """Test sanitization with multiple spaces."""
        chart = SunChart()
        assert chart._sanitize_filename("New   York   City") == "New_York_City"

    def test_create_chart_basic(self):
        """Test basic chart creation."""
        chart = SunChart()

        # Create sample data
        dates = [date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)]
        sunrise_times = [7.5, 7.6, 7.7]
        noon_times = [12.0, 12.0, 12.0]
        sunset_times = [16.5, 16.6, 16.7]

        fig = chart.create_chart(dates, sunrise_times, noon_times, sunset_times, "Test City", 2025)

        assert fig is not None
        assert len(fig.axes) > 0

    def test_create_chart_with_none_values(self):
        """Test chart creation with None values (polar regions)."""
        chart = SunChart()

        dates = [date(2025, 6, 1), date(2025, 6, 2), date(2025, 6, 3)]
        sunrise_times = [None, 2.5, 3.0]
        noon_times = [None, 12.5, 12.5]
        sunset_times = [None, 22.5, 23.0]

        fig = chart.create_chart(dates, sunrise_times, noon_times, sunset_times, "Arctic City", 2025)

        assert fig is not None
        assert len(fig.axes) > 0

    def test_create_chart_full_year(self):
        """Test chart creation with full year of data."""
        chart = SunChart()

        # Generate a full year of sample data
        dates = [date(2025, 1, 1 + i) if i < 31 else
                date(2025, 2, 1 + i - 31) if i < 59 else
                date(2025, 3, 1 + i - 59)
                for i in range(90)]

        sunrise_times = [7.0 + i * 0.01 for i in range(90)]
        noon_times = [12.0 + i * 0.005 for i in range(90)]
        sunset_times = [17.0 + i * 0.01 for i in range(90)]

        fig = chart.create_chart(dates, sunrise_times, noon_times, sunset_times, "Test City", 2025)

        assert fig is not None

    def test_save_chart(self, tmp_path):
        """Test saving chart to files."""
        chart = SunChart()

        # Create a simple chart
        dates = [date(2025, 1, 1), date(2025, 1, 2)]
        sunrise_times = [7.5, 7.6]
        noon_times = [12.0, 12.0]
        sunset_times = [16.5, 16.6]

        fig = chart.create_chart(dates, sunrise_times, noon_times, sunset_times, "Test City", 2025)

        # Save to temporary directory
        os.chdir(tmp_path)
        svg_file, png_file = chart.save_chart(fig, "test_chart", "Test City", 2025)

        # Check files were created
        assert os.path.exists(svg_file)
        assert os.path.exists(png_file)
        assert svg_file.endswith('.svg')
        assert png_file.endswith('.png')

    def test_save_chart_auto_filename(self, tmp_path):
        """Test saving chart with auto-generated filename."""
        chart = SunChart()

        dates = [date(2025, 1, 1), date(2025, 1, 2)]
        sunrise_times = [7.5, 7.6]
        noon_times = [12.0, 12.0]
        sunset_times = [16.5, 16.6]

        fig = chart.create_chart(dates, sunrise_times, noon_times, sunset_times, "London", 2025)

        os.chdir(tmp_path)
        svg_file, png_file = chart.save_chart(fig, "", "London", 2025)

        assert "London" in svg_file or "london" in svg_file.lower()
        assert "2025" in svg_file
        assert os.path.exists(svg_file)
        assert os.path.exists(png_file)


class TestPlotSunTimes:
    """Test cases for plot_sun_times convenience function."""

    def test_plot_sun_times(self, tmp_path):
        """Test the convenience function."""
        os.chdir(tmp_path)

        dates = [date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)]
        sunrise_times = [7.5, 7.6, 7.7]
        noon_times = [12.0, 12.0, 12.0]
        sunset_times = [16.5, 16.6, 16.7]

        svg_file, png_file = plot_sun_times(
            dates=dates,
            sunrise_times=sunrise_times,
            noon_times=noon_times,
            sunset_times=sunset_times,
            location_name="Test City",
            year=2025,
            filename_base="test_output"
        )

        assert os.path.exists(svg_file)
        assert os.path.exists(png_file)

    def test_plot_sun_times_default_year(self, tmp_path):
        """Test convenience function with default year."""
        os.chdir(tmp_path)

        dates = [date(2025, 1, 1), date(2025, 1, 2)]
        sunrise_times = [7.5, 7.6]
        noon_times = [12.0, 12.0]
        sunset_times = [16.5, 16.6]

        svg_file, png_file = plot_sun_times(
            dates=dates,
            sunrise_times=sunrise_times,
            noon_times=noon_times,
            sunset_times=sunset_times,
            location_name="Test City"
        )

        assert os.path.exists(svg_file)
        assert os.path.exists(png_file)
