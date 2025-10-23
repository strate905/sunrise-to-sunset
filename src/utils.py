"""
Sunrise to Sunset Chart - Utilities Module
Helper functions for user interaction and general utilities.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from typing import List, Optional
from src.geocoder import LocationData
import logging

logger = logging.getLogger(__name__)


def setup_logging(level: int = logging.INFO):
    """
    Configure logging for the application.

    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_user_input(prompt: str) -> str:
    """
    Get input from user with a prompt.

    Args:
        prompt: Prompt message to display

    Returns:
        User input string (stripped)
    """
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled by user.")
        raise SystemExit(0)


def display_locations(locations: List[LocationData]) -> None:
    """
    Display a numbered list of locations for user selection.

    Args:
        locations: List of LocationData objects to display
    """
    print("\nMultiple locations found. Please select one:")
    print("-" * 70)

    for i, loc in enumerate(locations, 1):
        # Build location description
        parts = [loc.name]
        if loc.state:
            parts.append(loc.state)
        if loc.country:
            parts.append(loc.country)

        location_str = ", ".join(parts)
        print(f"{i}. {location_str}")
        print(f"   Coordinates: ({loc.latitude:.4f}, {loc.longitude:.4f})")

    print("-" * 70)


def select_location(locations: List[LocationData]) -> Optional[LocationData]:
    """
    Let user select a location from a list.

    Args:
        locations: List of LocationData objects

    Returns:
        Selected LocationData or None if cancelled
    """
    if not locations:
        return None

    display_locations(locations)

    while True:
        try:
            choice = get_user_input(f"\nEnter your choice (1-{len(locations)}), or 'q' to quit: ")

            if choice.lower() == 'q':
                return None

            choice_num = int(choice)
            if 1 <= choice_num <= len(locations):
                return locations[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(locations)}.")

        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled by user.")
            return None


def format_time(hours: float) -> str:
    """
    Format decimal hours to HH:MM string.

    Args:
        hours: Time in decimal hours (0-24)

    Returns:
        Formatted time string (HH:MM)
    """
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h:02d}:{m:02d}"


def print_banner():
    """Print application banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║         Sunrise to Sunset Chart Generator                    ║
║         Generate beautiful sun time visualizations           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_success(svg_file: str, png_file: str):
    """
    Print success message with file paths.

    Args:
        svg_file: Path to SVG file
        png_file: Path to PNG file
    """
    print("\n" + "=" * 70)
    print("✓ Charts generated successfully!")
    print("=" * 70)
    print(f"SVG file: {svg_file}")
    print(f"PNG file: {png_file}")
    print("=" * 70)


def validate_coordinates(lat: float, lon: float) -> bool:
    """
    Validate coordinate ranges.

    Args:
        lat: Latitude
        lon: Longitude

    Returns:
        True if valid, False otherwise
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180
