# Sunrise to Sunset Chart

A Python command-line tool that generates beautiful visualizations of sunrise and sunset times throughout the year for any location on Earth.

## Features

- 📍 **Location Support**: Enter city names or precise coordinates (latitude, longitude)
- 🌍 **Global Coverage**: Works for any location worldwide with automatic timezone detection
- 📊 **Beautiful Charts**: Generates professional-looking charts in both SVG and PNG formats
- 🌐 **Multi-Language Support**: Automatically generates three versions - English, Arabic, and Japanese
- 🎨 **Clear Visualization**:
  - Orange line for sunrise times (warm morning light)
  - Gold line for solar noon times (bright midday sun at its zenith)
  - Crimson line for sunset times (deep sunset red)
  - Inverted y-axis with 00:00 at top and 24:00 at bottom
  - Hour-by-hour grid lines
  - Month markers on 1st and 15th of each month
- 🇯🇵 **Japanese Typography**: Full-width numbers (０-９) used in Japanese version for authentic formatting
- 🔄 **Ambiguity Resolution**: If city name matches multiple locations, presents a list to choose from
- ⚡ **Offline Calculations**: Uses astronomical calculations (no internet required after installation)
- 🧪 **Well-Tested**: Comprehensive test suite following industry best practices

## Requirements

- Python 3.12 or higher
- pip (Python package manager)

### Fonts

For consistent multilingual charts, install or copy Unicode-complete fonts into `fonts/` (e.g., IBM Plex Sans, IBM Plex Sans Arabic, Noto Sans CJK JP). The application auto-registers any `.ttf` or `.otf` files placed there and falls back to system fonts only if none are provided.

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd sunrise-to-sunset-in-python
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the script from the project root directory:

```bash
python -m src.main
```

Or make it executable and run directly:

```bash
chmod +x src/main.py
./src/main.py
```

### Example Sessions

#### Using a City Name

```
Enter city name or coordinates (lat, lon): Beirut

✓ Location: بيروت, محافظة بيروت, لبنان
  Coordinates: (33.8886, 35.4955)
  Timezone: Asia/Beirut

Calculating sunrise and sunset times for 2025...
✓ Calculated sun times for 365 days (365 with valid data)

Generating charts in English, Arabic, and Japanese...
  Generating English version...
  Generating Arabic version...
  Generating Japanese version...

======================================================================
✓ Charts generated successfully!
======================================================================

English:
  SVG: sunrise_sunset_Beirut_2025.svg
  PNG: sunrise_sunset_Beirut_2025.png

Arabic:
  SVG: sunrise_sunset_بيروت_2025_arabic.svg
  PNG: sunrise_sunset_بيروت_2025_arabic.png

Japanese:
  SVG: sunrise_sunset_ベイルート_2025_japanese.svg
  PNG: sunrise_sunset_ベイルート_2025_japanese.png
======================================================================
```

**Note**: The program automatically generates **three versions** of the chart - one in English, one in Arabic, and one in Japanese. Each version has its own labels, month names, and formatting conventions appropriate for that language.

#### Using Coordinates

```
Enter city name or coordinates (lat, lon): 35.6762, 139.6503

✓ Location: 東京都, 日本
  Coordinates: (35.6762, 139.6503)
  Timezone: Asia/Tokyo

Calculating sunrise and sunset times for 2025...
✓ Calculated sun times for 365 days (365 with valid data)

Generating charts in English, Arabic, and Japanese...
...
```

**Note**: When using coordinates for Japanese locations, the Japanese chart version will display all numbers in full-width format (e.g., ２０２５ instead of 2025, ００：００ instead of 00:00) following Japanese typography conventions.

#### Handling Ambiguous City Names

```
Enter city name or coordinates (lat, lon): Springfield

Multiple locations found. Please select one:
----------------------------------------------------------------------
1. Springfield, Massachusetts, United States
   Coordinates: (42.1015, -72.5898)
2. Springfield, Illinois, United States
   Coordinates: (39.7817, -89.6501)
3. Springfield, Missouri, United States
   Coordinates: (37.2090, -93.2923)
----------------------------------------------------------------------

Enter your choice (1-3), or 'q' to quit: 1
```

## Output Files

The program generates **six files** for each run (three language versions × two formats):

### English Version
- **SVG File**: `sunrise_sunset_London_2025.svg` (vector format, perfect for printing and scaling)
- **PNG File**: `sunrise_sunset_London_2025.png` (raster format, ready for presentations and sharing)

### Arabic Version
- **SVG File**: `sunrise_sunset_London_2025_arabic.svg` (with Arabic labels and RTL text)
- **PNG File**: `sunrise_sunset_London_2025_arabic.png`

### Japanese Version
- **SVG File**: `sunrise_sunset_London_2025_japanese.svg` (with full-width numbers)
- **PNG File**: `sunrise_sunset_London_2025_japanese.png`

All files are saved in the current working directory.

## Chart Details

The generated charts include:

- **Title**: Shows city name and year (with language-specific formatting)
- **X-axis** (`"Gregorian Month"`): Layouts months January–December with localized month names and vertical grid lines on the 1st and 15th.
  - Month names labeled (in each language: English, Arabic, or Japanese)
  - Vertical grid lines on 1st and 15th of each month
- **Y-axis** (`"Time of Day"`): 24-hour scale (00:00 at top, 24:00 at bottom) with horizontal hour grid lines and language-appropriate numerals.
  - **Inverted axis**: Early morning (00:00) at top, late night (24:00) at bottom
  - Horizontal grid lines for each hour
  - 24-hour time format
  - Japanese version uses full-width numbers (００：００, ０１：００, etc.)
- **Lines**:
  - **Orange line**: Sunrise times (warm morning light)
  - **Gold line**: Solar noon times (bright midday sun at its highest point/zenith - when shadow length equals object length)
  - **Crimson line**: Sunset times (deep sunset red)
- **Legend**: Clearly identifies each line (in each language)

## Language Support

The program automatically generates charts in **three languages**: English, Arabic, and Japanese. Each version has appropriate labels, month names, and formatting conventions.

### English Version
- **Month names**: January, February, March, etc.
- **Axis labels**: X = "Gregorian Month", Y = "Time of Day"
- **Legend**: "Sunrise", "Solar Noon", and "Sunset"
- **Numbers**: Standard ASCII digits (0-9)

### Arabic Version
- **Month names**: Full Arabic month names (كانون الثاني, شباط, آذار, etc.)
- **Axis labels**: X = "الشهر الميلادي" (Gregorian Month), Y = "وقت اليوم" (Time of Day)
- **Legend**: "شروق الشمس" (Sunrise), "الظهر" (Solar Noon), and "غروب الشمس" (Sunset)
- **Title**: Arabic format with proper RTL text rendering

### Japanese Version
- **Month names**: Japanese format with full-width numbers (１月, ２月, ３月, etc.)
- **Axis labels**: X = "西暦の月" (Gregorian Month), Y = "時刻" (Time of Day)
- **Legend**: "日の出" (Sunrise), "正午" (Solar Noon), and "日の入り" (Sunset)
- **Numbers**: Full-width Japanese digits (０-９) and punctuation (：, －)
- **Typography**: Authentic Japanese formatting with ideographic spaces

### Font Support and Multi-Script Rendering

The program includes comprehensive support for multiple writing systems with professional typography:

**Font Selection:**
- **English language**: Uses **IBM Plex Sans** with fallbacks to Noto Sans, DejaVu Sans, Arial, etc.
- **Arabic language**: Uses **IBM Plex Sans Arabic** with fallbacks to Noto Sans Arabic, Amiri, DejaVu Sans, etc.
- **Japanese language**: Uses **Noto Sans CJK JP** with fallbacks through Noto Sans JP, Source Han Sans, Harano Aji Gothic/Mincho, IBM Plex Sans JP, Droid Sans Japanese, WenQuanYi Zen Hei, Yu Gothic, Meiryo, and other Unicode-complete fonts (including Droid Sans Fallback and Arial Unicode MS).
- Automatically detects available fonts, registers any `.ttf`/`.otf` files placed in `fonts/`, and selects the best match.
- Ensures consistent, professional typography across all charts.

**RTL (Right-to-Left) Text Processing:**
- Uses `arabic-reshaper` to properly connect Arabic characters
- Uses `python-bidi` to apply bidirectional text algorithm
- Ensures Arabic text displays correctly in matplotlib charts
- Handles mixed Arabic/English text properly (e.g., "بيروت - Beirut")

**Japanese and CJK Support:**
- **Automatic generation**: Japanese version created automatically for all locations
- **Full-width numbers**: Uses authentic Japanese typography (０-９, ：, －) in Japanese charts
- **Font fallback chain**: Noto Sans CJK JP → Noto Sans JP → Noto Serif CJK JP → Source Han Sans → Source Han Sans JP → Harano Aji Gothic → Harano Aji Mincho → IBM Plex Sans JP → Droid Sans Japanese → WenQuanYi Zen Hei → Yu Gothic → Meiryo → Droid Sans Fallback → Arial Unicode MS → Latin font fallbacks
- **Unicode coverage**: Comprehensive support for kanji, hiragana, katakana, and full-width characters
- **Mixed scripts**: Properly displays both CJK and Latin characters together
- Examples: Tokyo (東京都), Beijing (北京), Seoul (서울)

**Technical Details:**
- **Arabic text** undergoes two transformations:
  1. **Reshaping**: Arabic characters are transformed to their proper contextual forms (initial, medial, final, isolated)
  2. **Bidirectional Algorithm**: Text direction is reversed for proper RTL display
- **Japanese text** undergoes full-width conversion:
  1. **Numbers**: ASCII digits (0-9) converted to full-width (U+FF10-FF19: ０-９)
  2. **Punctuation**: Colon (:), dash (-), and space converted to full-width equivalents
  3. **Typography**: Uses ideographic space (U+3000) for proper character alignment
- **Font fallback**: Automatically selects the best available font for each script from the font priority list

**Installing Recommended Fonts:**

For the best typography with all scripts, install these fonts on your system:

**IBM Plex Fonts (for Latin and Arabic):**
- **Linux**: `sudo apt-get install fonts-ibm-plex` or `sudo dnf install ibm-plex-fonts-all` (Fedora)
- **macOS**: `brew install --cask font-ibm-plex`
- **Windows**: Download from [IBM Plex GitHub](https://github.com/IBM/plex)

**Japanese/CJK Fonts:**

The program works with several Japanese fonts. Most Linux systems already have suitable fonts:

- **Noto Sans CJK JP**: Google's high-quality CJK font family with full-width support
- **Source Han Sans / Harano Aji Gothic**: Adobe/IPA professional Japanese fonts with broad glyph coverage
- **IBM Plex Sans JP** or **Droid Sans Fallback**: Helpful fallbacks for mixed Latin/CJK text

To install additional Japanese fonts:
```bash
# Fedora Linux (already has Droid Sans Fallback and Harano Aji fonts)
sudo dnf install google-noto-sans-cjk-fonts

# Debian/Ubuntu
sudo apt-get install fonts-noto-cjk fonts-droid-fallback

# macOS
brew install --cask font-noto-sans-cjk-jp

# Windows
# Download from https://www.google.com/get/noto/ and install manually
```

**Important Note:**
- The program automatically generates Japanese versions for all locations
- If full-width numbers don't display correctly in PNG files, they will still be correct in SVG files
- SVG files can be opened in web browsers or vector graphics editors with proper font rendering
- Most modern Linux systems (especially Fedora) come with suitable Japanese fonts pre-installed

After installing new fonts, you may need to clear matplotlib's font cache:
```bash
rm -rf ~/.cache/matplotlib
```


## Project Structure

```
sunrise-to-sunset-in-python/
├── SPECIFICATIONS.md          # Detailed project specifications
├── README.md                  # This file
├── LICENSE                    # GPLv3 license
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── src/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Main entry point
│   ├── calculator.py         # Sunrise/sunset calculations
│   ├── geocoder.py           # Location resolution
│   ├── plotter.py            # Chart generation
│   └── utils.py              # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_geocoder.py
│   ├── test_plotter.py
│   └── test_utils.py
└── examples/                  # Example output files (optional)
```

## Running Tests

The project includes a comprehensive test suite. To run the tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_calculator.py

# Run tests excluding slow network tests
pytest -m "not slow"
```

## Dependencies

### Core Dependencies
- **astral** (≥3.2): Astronomical calculations for sunrise/sunset times
- **matplotlib** (≥3.8.0): Chart generation and visualization
- **geopy** (≥2.4.0): Geocoding and location services
- **timezonefinder** (≥6.0.0): Timezone detection from coordinates

### Arabic Text Support
- **arabic-reshaper** (≥3.0.0): Reshapes Arabic characters for proper display
- **python-bidi** (≥0.4.2): Bidirectional text algorithm for RTL languages

### Testing Dependencies
- **pytest** (≥7.4.0): Testing framework
- **pytest-cov** (≥4.1.0): Code coverage reporting

## Special Cases

### Polar Regions

The program gracefully handles locations in polar regions where the sun may not rise or set for extended periods (midnight sun and polar night). Days without valid sunrise/sunset data are handled appropriately in the calculations and visualizations.

### Timezone Handling

The program automatically detects the correct timezone for any location and uses it for accurate sunrise/sunset calculations. Times are displayed in the local timezone of the selected location.

### Location Name Display

The program displays location names in their local format (as returned by the geocoding service):

- **City name input**: The chart displays the official geocoded name in its local format
  - Example: "Beirut" → "بيروت, محافظة بيروت, لبنان" (Arabic)
  - Example: "Tokyo" → "東京都, 日本" (Japanese)
  - Example: "Cairo" → "القاهرة, محافظة القاهرة, مصر" (Arabic)
- **Coordinate input**: Uses the geocoded location name for that coordinate

**Multi-Script Support**:
- **Arabic locations**: RTL text processing ensures proper character connections and right-to-left text direction
- **Japanese locations**: Full CJK character support with proper kanji/kana rendering
- **Mixed scripts**: Location names can contain multiple scripts (e.g., "東京都" with "Japan")

**Note**: Location names appear in all three chart versions (English, Arabic, and Japanese) using the same local format returned by the geocoding service.

## Troubleshooting

### "Could not find location" Error

- Check the spelling of the city name
- Try using a larger city nearby
- Use coordinates instead: `latitude, longitude`

### Network Connection Issues

- The geocoding service (for city name lookup) requires internet connection
- Once you have coordinates, astronomical calculations work offline
- Consider using coordinates directly if you're offline

### Import Errors

Make sure you're running from the project root directory:
```bash
# Correct
python -m src.main

# Incorrect
cd src
python main.py  # This will fail with import errors
```

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

## Acknowledgments

- **Astral Library**: For providing accurate astronomical calculations
- **Matplotlib**: For powerful and flexible plotting capabilities
- **Geopy**: For reliable geocoding services
- **Timezonefinder**: For efficient timezone detection

## Version

Current version: 1.0.0

## Author

Sunrise to Sunset Chart Contributors

---

**Enjoy visualizing the sun's journey across the sky! ☀️🌅🌇**
