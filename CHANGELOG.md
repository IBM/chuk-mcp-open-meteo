# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **New Tool**: `batch_interpret_weather_codes` - Interpret multiple WMO weather codes in a single call
  - Comma-separated input: `"3,51,61,95"` → all interpretations at once
  - Eliminates N sequential `interpret_weather_code` calls after batch forecasts
  - Returns `BatchWeatherCodeResponse` Pydantic model
  - Handles unknown codes and invalid input gracefully
- **New Tool**: `interpret_weather_code` - Translate WMO weather codes into human-readable descriptions
  - Returns Pydantic `WeatherCodeInterpretation` model
  - Comprehensive documentation of all weather codes (0-99)
  - Includes severity categories for better LLM understanding
- **Enhanced Documentation**: Massively improved docstrings for all tools
  - Added "Tips for LLMs" sections with guidance on tool usage
  - Detailed parameter descriptions with examples
  - Common use cases and best practices
  - Weather code reference in forecast tool
  - Wave height and period interpretation guides for marine forecast
  - Activity recommendations based on conditions
- **Enhanced Pydantic Models**: All field descriptions now include LLM-friendly context
  - `HourlyMarine`: Wave height ranges (0-0.5m=calm, 0.5-1.5m=small, etc.)
  - `HourlyMarine`: Wave period quality indicators (<8s=choppy, 8-12s=good, 12s+=excellent)
  - `CurrentWeather`: Wind direction explanations (0=from North, 90=from East, etc.)
  - `CurrentWeather`: Weather code quick reference in field description
  - `HourlyWeather`: Clarified precipitation types and units
  - `DailyWeather`: Added descriptions for daily aggregates
  - All direction fields now explain meteorological convention
  - All models include docstrings with usage guidance

### Changed
- Updated Pydantic models to use ConfigDict instead of deprecated class-based Config
- Improved test coverage to 99% (all files >90%)
- Added comprehensive tests for all API parameters and edge cases
- Enhanced all tool docstrings with LLM-friendly guidance
- Added comprehensive weather code database (WMO codes 0-99)
- **`geocode_location` docstring**: Added warning about simpler search terms
  - Open-Meteo API works better with just city names (e.g., "Mullion" vs "Mullion, Cornwall")
  - Added example showing fallback pattern when complex queries return no results

### Fixed
- Removed `uv.lock` from `.gitignore` to fix CI/CD cache dependency resolution
- Improved `geocode_location` guidance to prevent "no results" issues with qualified location names

## [1.1.0] - 2024-11-22

### Added
- **Pydantic Models**: All API responses now use Pydantic v2 models for type safety
  - `WeatherForecast`, `CurrentWeather`, `HourlyWeather`, `DailyWeather`
  - `GeocodingResponse`, `GeocodingResult`
  - `HistoricalWeather`
  - `AirQualityResponse`, `HourlyAirQuality`
  - `MarineForecast`, `HourlyMarine`, `DailyMarine`
- Full type hints throughout the codebase
- `MANIFEST.in` for proper package distribution
- `mypy.ini` for type checking configuration
- Comprehensive Pydantic model documentation in models.py

### Changed
- **Breaking**: All tool functions now return Pydantic models instead of dictionaries
- Tools are now fully async-native (already were, but now enforced by Pydantic)
- Improved type safety and IDE autocomplete support
- Better validation of API responses

### Fixed
- Server now defaults to STDIO transport mode for proper MCP client compatibility
- Logging configured to use stderr and ERROR level in STDIO mode (no noise in JSON-RPC stream)
- Corrected API endpoints:
  - Geocoding: Now uses `geocoding-api.open-meteo.com` (was incorrect)
  - Historical: Now uses `archive-api.open-meteo.com` (was incorrect)
- Python version requirement updated to >=3.11 (matches chuk-mcp-server dependency)
- Bare except clauses replaced with specific exception handling
- Code formatted with ruff

## [1.0.0] - 2024-11-22

## [1.0.0] - 2024-11-22

### Added
- Initial release of chuk-mcp-open-meteo - The best weather MCP server ever!
- **get_weather_forecast** tool for comprehensive weather forecasts
  - Current weather conditions
  - Hourly forecasts (up to 16 days)
  - Daily forecasts
  - 50+ customizable weather variables
  - Multiple unit systems (celsius/fahrenheit, km/h/mph/m/s/knots)
  - Automatic timezone detection
- **geocode_location** tool for location search and coordinate lookup
  - Worldwide location search
  - Multi-language support
  - Coordinates, elevation, timezone information
  - Population and administrative data
- **get_historical_weather** tool for historical weather data
  - Data from 1940 onwards (location-dependent)
  - Same comprehensive variables as forecasts
  - Hourly and daily aggregations
  - Perfect for climate analysis
- **get_air_quality** tool for air quality monitoring
  - PM2.5, PM10 particulate matter
  - CO, NO2, SO2, O3 gas concentrations
  - European and US AQI indices
  - Pollen data (multiple species)
  - UV index and aerosol optical depth
- **get_marine_forecast** tool for marine weather
  - Wave height, direction, and period
  - Wind waves and swell waves (separate data)
  - Ocean current velocity and direction
  - Up to 16-day forecasts
- Comprehensive documentation
  - README with detailed examples
  - Usage examples document
  - Contributing guidelines
  - Quick start guide
- Full test suite with pytest
  - Async test support
  - Coverage reporting
  - Integration tests for all tools
- CI/CD with GitHub Actions
  - Multi-platform testing (Ubuntu, Windows, macOS)
  - Multi-version testing (Python 3.11, 3.12, 3.13)
  - Automated releases
  - PyPI publishing
- Docker support
  - Multi-stage Dockerfile
  - Optimized image size
  - Non-root user for security
  - Health checks
- Fly.io deployment configuration
  - Auto-scaling
  - Minimal resource usage
  - HTTP service support
- Development tooling
  - Comprehensive Makefile
  - Code formatting (ruff)
  - Type checking (mypy)
  - Security scanning (bandit)
  - Coverage reporting
- Claude Desktop integration examples
- MIT License

### Technical Details
- Built on chuk-mcp-server framework
- Async/await throughout for optimal performance
- Type-safe with full type hints
- Automatic JSON-RPC schema generation
- No API key required (uses free Open-Meteo API)
- Global weather coverage with 25+ weather models

### Documentation
- Comprehensive README
- Detailed usage examples
- API reference in docstrings
- Contributing guidelines
- Quick start guide
- Project summary
- Example configurations

### Infrastructure
- Multi-platform CI/CD
- Automated testing and quality checks
- Automated releases and publishing
- Docker containerization
- Cloud deployment ready (Fly.io)
