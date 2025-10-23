#!/usr/bin/env python3
"""
Sunrise to Sunset Chart - Main Entry Point
Generate sunrise and sunset charts for any location.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import sys
import logging
from datetime import datetime
from src.geocoder import GeocoderService, LocationData
from src.calculator import SunCalculator
from src.plotter import plot_sun_times
from src.utils import (
    setup_logging,
    get_user_input,
    select_location,
    print_banner,
    print_success
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    # Setup logging
    setup_logging(level=logging.WARNING)  # Only show warnings and errors to user

    # Print banner
    print_banner()

    try:
        # Initialize geocoder service
        geocoder = GeocoderService()

        # Get user input
        user_input = get_user_input("Enter city name or coordinates (lat, lon): ")

        if not user_input:
            print("Error: No input provided.")
            return 1

        # Resolve location
        print("\nResolving location...")
        location, matches = geocoder.resolve_location(user_input)

        # Handle multiple matches
        if location is None and matches:
            location = select_location(matches)
            if location is None:
                print("No location selected. Exiting.")
                return 0
        elif location is None:
            print(f"Error: Could not find location '{user_input}'.")
            print("Please check the spelling or try using coordinates (lat, lon).")
            return 1

        # Display selected location
        print(f"\n✓ Location: {location}")
        print(f"  Coordinates: ({location.latitude:.4f}, {location.longitude:.4f})")
        print(f"  Timezone: {location.timezone}")

        # Build localized display names for each output language
        localized_names = {
            'english': location.get_localized_name('english'),
            'arabic': location.get_localized_name('arabic'),
            'japanese': location.get_localized_name('japanese')
        }
        # Default display name for CLI feedback prefers English when available
        display_name = localized_names['english']

        # Calculate sunrise/sunset times
        year = datetime.now().year
        print(f"\nCalculating sunrise and sunset times for {year}...")

        calculator = SunCalculator(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=location.timezone
        )

        dates, sunrise_times, noon_times, sunset_times = calculator.calculate_year(year)

        # Check if we have valid data
        valid_count = sum(1 for s in sunrise_times if s is not None)
        if valid_count == 0:
            print(f"Error: Could not calculate sun times for {display_name}.")
            print("This location may be in a polar region where the sun doesn't rise/set regularly.")
            return 1

        print(f"✓ Calculated sun times for {len(dates)} days ({valid_count} with valid data)")

        # Generate charts in all three languages
        print("\nGenerating charts in English, Arabic, and Japanese...")

        generated_files = []

        # Generate English version
        print("  Generating English version...")
        svg_file, png_file = plot_sun_times(
            dates=dates,
            sunrise_times=sunrise_times,
            noon_times=noon_times,
            sunset_times=sunset_times,
            location_name=localized_names['english'],
            year=year,
            language='english'
        )
        generated_files.extend([('English', svg_file, png_file)])

        # Generate Arabic version
        print("  Generating Arabic version...")
        svg_file, png_file = plot_sun_times(
            dates=dates,
            sunrise_times=sunrise_times,
            noon_times=noon_times,
            sunset_times=sunset_times,
            location_name=localized_names['arabic'],
            year=year,
            language='arabic'
        )
        generated_files.extend([('Arabic', svg_file, png_file)])

        # Generate Japanese version
        print("  Generating Japanese version...")
        svg_file, png_file = plot_sun_times(
            dates=dates,
            sunrise_times=sunrise_times,
            noon_times=noon_times,
            sunset_times=sunset_times,
            location_name=localized_names['japanese'],
            year=year,
            language='japanese'
        )
        generated_files.extend([('Japanese', svg_file, png_file)])

        # Display success for all versions
        print("\n" + "=" * 70)
        print("✓ Charts generated successfully!")
        print("=" * 70)
        for lang, svg, png in generated_files:
            print(f"\n{lang}:")
            print(f"  SVG: {svg}")
            print(f"  PNG: {png}")
        print("=" * 70)

        return 0

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130
    except Exception as e:
        logger.exception("An error occurred")
        print(f"\nError: {e}")
        print("Please check your input and try again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
