"""
Sunrise to Sunset Chart - Plotter Module
Handles chart generation and visualization.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

from datetime import date
from pathlib import Path
from typing import List, Optional, Dict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.font_manager as fm
import numpy as np
import logging

# Arabic text support for RTL (Right-to-Left) rendering
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False
    logging.warning("Arabic text libraries not installed. Arabic text may not display correctly.")

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = PROJECT_ROOT / "fonts"


def _register_project_fonts(font_directory: Path) -> List[str]:
    """
    Register bundled fonts with matplotlib so they are always available.

    Args:
        font_directory: Directory containing .ttf/.otf files.

    Returns:
        List of human-readable font names that were registered.
    """
    if not font_directory.exists():
        return []

    registered_fonts: List[str] = []
    font_files = sorted(
        list(font_directory.glob("*.ttf")) + list(font_directory.glob("*.otf"))
    )

    for font_file in font_files:
        try:
            font_entry = fm.fontManager.addfont(str(font_file))
            # addfont returns the path when matplotlib < 3.6, FontEntry in newer versions
            if hasattr(font_entry, "name"):
                registered_fonts.append(font_entry.name)
            else:
                # Best effort: resolve name via FontProperties
                font_name = fm.FontProperties(fname=str(font_file)).get_name()
                if font_name:
                    registered_fonts.append(font_name)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.warning(f"Could not register font '{font_file.name}': {exc}")

    if registered_fonts:
        try:  # pragma: no cover - optional refresh depending on Matplotlib version
            fm._load_fontmanager(try_read_cache=False)  # type: ignore[attr-defined]
        except Exception:
            pass

    return registered_fonts


REGISTERED_FONTS = _register_project_fonts(FONTS_DIR)
if REGISTERED_FONTS:
    logger.info("Registered bundled fonts: %s", ", ".join(REGISTERED_FONTS))

# Arabic month names
# ARABIC_MONTHS = {
#     1: 'كانون الثاني', # January
#     2: 'شباط',         # February
#     3: 'آذار',         # March
#     4: 'نيسان',        # April
#     5: 'أيار',         # May
#     6: 'حزيران',       # June
#     7: 'تموز',         # July
#     8: 'آب',           # August
#     9: 'أيلول',        # September
#     10: 'تشرين الأول',  # October
#     11: 'تشرين الثاني',# November
#     12: 'كانون الأول'   # December
# }

# Arabic month names
ARABIC_MONTHS = {
    1: 'كانون الثاني', # January
    2: 'شباط',         # February
    3: 'آذار',         # March
    4: 'نيسان',        # April
    5: 'أيار',         # May
    6: 'حزيران',       # June
    7: 'تموز',         # July
    8: 'آب',           # August
    9: 'أيلول',        # September
    10: 'تشرين الأول',  # October
    11: 'تشرين الثاني',# November
    12: 'كانون الأول'   # December
}

# Japanese month names (using full-width numbers)
JAPANESE_MONTHS = {
    1: '１月',   # January
    2: '２月',   # February
    3: '３月',   # March
    4: '４月',   # April
    5: '５月',   # May
    6: '６月',   # June
    7: '７月',   # July
    8: '８月',   # August
    9: '９月',   # September
    10: '１０月',  # October
    11: '１１月',  # November
    12: '１２月'   # December
}

# Arabic text translations
ARABIC_TEXT = {
    'sunrise': 'شروق الشمس',
    'noon': 'الظهر',
    'sunset': 'غروب الشمس',
    'x_axis_label': 'الشهر الميلادي',
    'time_of_day': 'وقت اليوم',
    'title_template': '{location} - رسم بياني لشروق وغروب الشمس لعام {year}'
}

# Japanese text translations
JAPANESE_TEXT = {
    'sunrise': '日の出',
    'noon': '正午',
    'sunset': '日の入り',
    'x_axis_label': '西暦の月',
    'time_of_day': '時刻',
    'title_template': '{location} - {year}年の日の出と日の入りのグラフ'
}

# English text (for clarity)
ENGLISH_TEXT = {
    'sunrise': 'Sunrise',
    'noon': 'Solar Noon',
    'sunset': 'Sunset',
    'x_axis_label': 'Gregorian Month',
    'time_of_day': 'Time of Day',
    'title_template': '{location} - Sunrise and Sunset Graph for {year}'
}

# Preferred font families per script. Matplotlib will automatically fall back
# through the list until it finds one installed/registered.
FONT_FALLBACKS: Dict[str, List[str]] = {
    'default': [
        'IBM Plex Sans',
        'Noto Sans',
        'DejaVu Sans',
        'Arial',
        'Liberation Sans',
        'FreeSans'
    ],
    'arabic': [
        'IBM Plex Sans Arabic',
        'Noto Sans Arabic',
        'Amiri',
        'DejaVu Sans',
        'Arial Unicode MS',
        'Arial',
        'Liberation Sans',
        'FreeSans'
    ],
    'cjk': [
        'Noto Sans CJK JP',
        'Noto Sans JP',
        'Noto Serif CJK JP',
        'Source Han Sans',
        'Source Han Sans JP',
        'Harano Aji Gothic',
        'Harano Aji Mincho',
        'IBM Plex Sans JP',
        'Droid Sans Japanese',
        'WenQuanYi Zen Hei',
        'Yu Gothic',
        'Meiryo',
        'Droid Sans Fallback',
        'Arial Unicode MS',
        'Noto Sans',
        'IBM Plex Sans',
        'Source Sans Pro',
        'DejaVu Sans',
        'Arial',
        'Liberation Sans',
        'FreeSans'
    ],
}


def to_fullwidth_japanese(text: str) -> str:
    """
    Convert ASCII numbers and punctuation to full-width Japanese characters.

    Args:
        text: Text containing ASCII numbers and punctuation

    Returns:
        Text with full-width Japanese characters
    """
    # Mapping of ASCII to full-width characters
    # Full-width forms are used in Japanese typography for proper alignment
    fullwidth_map = {
        '0': '０', '1': '１', '2': '２', '3': '３', '4': '４',
        '5': '５', '6': '６', '7': '７', '8': '８', '9': '９',
        ':': '：',  # U+FF1A - Full-width colon
        '-': '－',  # U+FF0D - Full-width hyphen-minus (used in Japanese)
        '/': '／',  # U+FF0F - Full-width solidus
        ' ': '　'   # U+3000 - Ideographic space
    }

    result = []
    for char in str(text):
        result.append(fullwidth_map.get(char, char))
    return ''.join(result)


def contains_arabic(text: str) -> bool:
    """
    Check if a string contains Arabic characters.

    Args:
        text: The text to check

    Returns:
        True if the text contains Arabic characters, False otherwise
    """
    # Arabic Unicode range: \u0600-\u06FF (basic), \u0750-\u077F (supplement)
    # \u08A0-\u08FF (extended), \uFB50-\uFDFF (presentation forms A)
    # \uFE70-\uFEFF (presentation forms B)
    import re
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(arabic_pattern.search(text))


def contains_cjk(text: str) -> bool:
    """
    Check if a string contains CJK (Chinese, Japanese, Korean) characters.

    Args:
        text: The text to check

    Returns:
        True if the text contains CJK characters, False otherwise
    """
    # CJK Unicode ranges:
    # \u4E00-\u9FFF: CJK Unified Ideographs
    # \u3040-\u309F: Hiragana
    # \u30A0-\u30FF: Katakana
    # \uAC00-\uD7AF: Hangul Syllables
    # \u3400-\u4DBF: CJK Unified Ideographs Extension A
    import re
    cjk_pattern = re.compile(r'[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF\u3400-\u4DBF]')
    return bool(cjk_pattern.search(text))


def reshape_arabic_text(text: str) -> str:
    """
    Reshape Arabic text for proper display in matplotlib.

    This function applies the following transformations:
    1. Reshapes Arabic characters to their proper contextual forms
    2. Applies the bidirectional algorithm for RTL text

    Args:
        text: The text to reshape (can contain Arabic, English, or mixed)

    Returns:
        Reshaped text ready for display in matplotlib
    """
    if not ARABIC_SUPPORT:
        logger.warning("Arabic text support not available - text may display incorrectly")
        return text

    try:
        # Reshape Arabic text (handles contextual forms)
        reshaped_text = arabic_reshaper.reshape(text)
        # Apply bidirectional algorithm (handles RTL)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception as e:
        logger.error(f"Error reshaping Arabic text: {e}")
        return text


class SunChart:
    """Creates and saves sunrise/sunset charts."""

    # Color scheme
    SUNRISE_COLOR = '#FFA500'  # Orange (warm morning light)
    NOON_COLOR = '#FFD700'     # Gold (bright midday sun)
    SUNSET_COLOR = '#DC143C'   # Crimson (deep sunset red)
    GRID_COLOR = '#D3D3D3'     # Light gray
    BACKGROUND_COLOR = '#FFFFFF'  # White

    def __init__(self, figsize: tuple = (14, 8), dpi: int = 100):
        """
        Initialize the chart plotter.

        Args:
            figsize: Figure size in inches (width, height)
            dpi: Dots per inch for the output image
        """
        self.figsize = figsize
        self.dpi = dpi

    def _configure_font(self, script_type: str = 'default'):
        """
        Configure matplotlib to use the appropriate font based on script type.

        Args:
            script_type: Type of script - 'arabic', 'cjk', or 'default'
        """
        # Get available fonts after registering bundled assets
        available_fonts = {f.name for f in fm.fontManager.ttflist}

        language_name = {
            'arabic': "Arabic",
            'cjk': "CJK (Chinese/Japanese/Korean)",
        }.get(script_type, "English")

        font_preferences = FONT_FALLBACKS.get(script_type, FONT_FALLBACKS['default'])
        font_list = [font for font in font_preferences if font in available_fonts]

        if not font_list:
            font_list = ['DejaVu Sans']
            logger.warning(
                "Falling back to DejaVu Sans; no preferred fonts found for %s text",
                language_name
            )

        # Log the selected fonts
        logger.info(f"Using font fallback chain for {language_name}: {', '.join(font_list[:3])}")

        # Configure matplotlib to use the font fallback list
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = font_list

        # Fix minus sign display
        plt.rcParams['axes.unicode_minus'] = False

    def create_chart(self, dates: List[date], sunrise_times: List[float],
                    noon_times: List[float], sunset_times: List[float], location_name: str,
                    year: Optional[int] = None, language: str = 'english') -> Figure:
        """
        Create a sunrise/noon/sunset chart.

        Args:
            dates: List of date objects
            sunrise_times: List of sunrise times as decimal hours (0-24)
            noon_times: List of solar noon times as decimal hours (0-24)
            sunset_times: List of sunset times as decimal hours (0-24)
            location_name: Name of the location
            year: Year (defaults to dates[0].year if not provided)
            language: Language for labels and months ('english', 'arabic', or 'japanese')

        Returns:
            Matplotlib Figure object
        """
        if year is None and dates:
            year = dates[0].year

        # Determine which script type is needed based on language
        if language == 'arabic':
            script_type = 'arabic'
        elif language == 'japanese':
            script_type = 'cjk'
        else:
            script_type = 'default'

        # Configure font for the selected language
        self._configure_font(script_type)

        # Select language-specific text
        if language == 'arabic':
            text_dict = ARABIC_TEXT
        elif language == 'japanese':
            text_dict = JAPANESE_TEXT
        else:
            text_dict = ENGLISH_TEXT

        # Format the title with original (non-reshaped) location name
        # For Japanese, convert year to full-width numbers
        if language == 'japanese':
            year_display = to_fullwidth_japanese(str(year))
        else:
            year_display = year
        title_raw = text_dict['title_template'].format(location=location_name, year=year_display)

        # Prepare display text (reshape Arabic if needed, convert Japanese to full-width)
        if language == 'arabic':
            # Arabic language: reshape all text
            sunrise_label = reshape_arabic_text(text_dict['sunrise'])
            noon_label = reshape_arabic_text(text_dict['noon'])
            sunset_label = reshape_arabic_text(text_dict['sunset'])
            xlabel = reshape_arabic_text(text_dict['x_axis_label'])
            ylabel = reshape_arabic_text(text_dict['time_of_day'])
            # Reshape entire title (includes Arabic template + location)
            title_text = reshape_arabic_text(title_raw)
        elif language == 'japanese':
            # Japanese: use text as-is (already in Japanese)
            sunrise_label = text_dict['sunrise']
            noon_label = text_dict['noon']
            sunset_label = text_dict['sunset']
            xlabel = text_dict['x_axis_label']
            ylabel = text_dict['time_of_day']
            # Convert ASCII punctuation in title to full-width (dash, spaces, etc.)
            title_text = to_fullwidth_japanese(title_raw)
        else:
            # English: use text as-is
            sunrise_label = text_dict['sunrise']
            noon_label = text_dict['noon']
            sunset_label = text_dict['sunset']
            xlabel = text_dict['x_axis_label']
            ylabel = text_dict['time_of_day']
            title_text = title_raw

        # Create figure and axis
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        fig.patch.set_facecolor(self.BACKGROUND_COLOR)
        ax.set_facecolor(self.BACKGROUND_COLOR)

        # Convert dates to ordinal for plotting
        date_nums = [d.toordinal() for d in dates]

        # Filter out None values for polar regions
        valid_sunrise = [(d, t) for d, t in zip(date_nums, sunrise_times) if t is not None]
        valid_noon = [(d, t) for d, t in zip(date_nums, noon_times) if t is not None]
        valid_sunset = [(d, t) for d, t in zip(date_nums, sunset_times) if t is not None]

        if valid_sunrise:
            sunrise_dates, sunrise_values = zip(*valid_sunrise)
            ax.plot(sunrise_dates, sunrise_values, color=self.SUNRISE_COLOR,
                   linewidth=2.5, label=sunrise_label, zorder=3)

        if valid_noon:
            noon_dates, noon_values = zip(*valid_noon)
            ax.plot(noon_dates, noon_values, color=self.NOON_COLOR,
                   linewidth=2.5, label=noon_label, zorder=3)

        if valid_sunset:
            sunset_dates, sunset_values = zip(*valid_sunset)
            ax.plot(sunset_dates, sunset_values, color=self.SUNSET_COLOR,
                   linewidth=2.5, label=sunset_label, zorder=3)

        # Set title
        ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20)

        # Set labels
        ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')

        # Configure x-axis (dates)
        ax.set_xlim(dates[0].toordinal(), dates[-1].toordinal())

        # Create month boundaries for vertical lines
        month_dates = []
        month_labels = []
        for month in range(1, 13):
            # 1st of each month
            first_day = date(year, month, 1)
            month_dates.append(first_day.toordinal())
            month_labels.append(first_day.strftime('%b'))

            # 15th of each month
            fifteenth = date(year, month, 15)
            month_dates.append(fifteenth.toordinal())

        # Draw vertical lines for 1st and 15th of each month
        for month_date in month_dates:
            ax.axvline(x=month_date, color=self.GRID_COLOR, linewidth=0.8,
                      linestyle='-', alpha=0.7, zorder=1)

        # Set x-axis ticks to show months
        month_firsts = [date(year, m, 1).toordinal() for m in range(1, 13)]
        if language == 'arabic':
            # Use Arabic month names (reshaped for proper RTL display)
            month_names = [reshape_arabic_text(ARABIC_MONTHS[m]) for m in range(1, 13)]
        elif language == 'japanese':
            # Use Japanese month names
            month_names = [JAPANESE_MONTHS[m] for m in range(1, 13)]
        else:
            # Use English month names
            month_names = [date(year, m, 1).strftime('%B') for m in range(1, 13)]
        ax.set_xticks(month_firsts)
        ax.set_xticklabels(month_names, rotation=45, ha='right')

        # Configure y-axis (time of day)
        ax.set_ylim(0, 24)
        hours = list(range(0, 25, 1))  # 0 to 24
        ax.set_yticks(hours)

        # Format time labels based on language
        if language == 'japanese':
            # Use full-width Japanese numbers
            time_labels = [to_fullwidth_japanese(f"{h:02d}:00") for h in hours]
        else:
            time_labels = [f"{h:02d}:00" for h in hours]
        ax.set_yticklabels(time_labels)

        # Invert y-axis so 00:00 is at top and 24:00 is at bottom
        ax.invert_yaxis()

        # Draw horizontal lines for each hour
        for hour in hours:
            ax.axhline(y=hour, color=self.GRID_COLOR, linewidth=0.8,
                      linestyle='-', alpha=0.7, zorder=1)

        # Add legend
        ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

        # Add grid (lighter, behind everything)
        ax.grid(True, which='major', color=self.GRID_COLOR, linewidth=0.5,
               linestyle=':', alpha=0.3, zorder=0)

        # Adjust layout to prevent label cutoff
        plt.tight_layout()

        return fig

    def save_chart(self, fig: Figure, filename_base: str, location_name: str, year: int):
        """
        Save the chart in SVG and PNG formats.

        Args:
            fig: Matplotlib Figure object
            filename_base: Base filename (without extension)
            location_name: Name of the location
            year: Year
        """
        # Sanitize location name for filename
        safe_location = self._sanitize_filename(location_name)

        # Create filenames
        if not filename_base:
            filename_base = f"sunrise_sunset_{safe_location}_{year}"

        svg_file = f"{filename_base}.svg"
        png_file = f"{filename_base}.png"

        # Save as SVG
        try:
            fig.savefig(svg_file, format='svg', dpi=self.dpi,
                       bbox_inches='tight', facecolor=self.BACKGROUND_COLOR)
            logger.info(f"Saved SVG chart: {svg_file}")
        except Exception as e:
            logger.error(f"Failed to save SVG: {e}")
            raise

        # Save as PNG
        try:
            fig.savefig(png_file, format='png', dpi=self.dpi,
                       bbox_inches='tight', facecolor=self.BACKGROUND_COLOR)
            logger.info(f"Saved PNG chart: {png_file}")
        except Exception as e:
            logger.error(f"Failed to save PNG: {e}")
            raise

        return svg_file, png_file

    def _sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string for use in filenames.

        Args:
            name: String to sanitize

        Returns:
            Sanitized string safe for filenames
        """
        # Remove or replace invalid filename characters
        invalid_chars = '<>:"/\\|?*,'
        for char in invalid_chars:
            name = name.replace(char, '_')

        # Remove extra spaces and replace spaces with underscores
        name = '_'.join(name.split())

        return name


def plot_sun_times(dates: List[date], sunrise_times: List[float],
                  noon_times: List[float], sunset_times: List[float], location_name: str,
                  year: Optional[int] = None, filename_base: str = "",
                  language: str = 'english') -> tuple:
    """
    Convenience function to create and save a sun times chart.

    Args:
        dates: List of date objects
        sunrise_times: List of sunrise times as decimal hours
        noon_times: List of solar noon times as decimal hours
        sunset_times: List of sunset times as decimal hours
        location_name: Name of the location
        year: Year (optional)
        filename_base: Base filename (optional)
        language: Language for labels ('english', 'arabic', or 'japanese')

    Returns:
        Tuple of (svg_filename, png_filename)
    """
    if year is None and dates:
        year = dates[0].year

    plotter = SunChart()
    fig = plotter.create_chart(dates, sunrise_times, noon_times, sunset_times, location_name, year, language)

    # Add language suffix to filename if not English
    if language != 'english' and filename_base:
        base, ext = filename_base.rsplit('.', 1) if '.' in filename_base else (filename_base, '')
        filename_base = f"{base}_{language}" + (f".{ext}" if ext else '')
    elif language != 'english':
        # Generate filename with language suffix
        sanitized_location = plotter._sanitize_filename(location_name)
        filename_base = f"sunrise_sunset_{sanitized_location}_{year}_{language}"

    svg_file, png_file = plotter.save_chart(fig, filename_base, location_name, year)

    # Close the figure to free memory
    plt.close(fig)

    return svg_file, png_file
