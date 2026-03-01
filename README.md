# Chuk MCP Open-Meteo

**The best weather MCP server ever** - A comprehensive Model Context Protocol (MCP) server for accessing Open-Meteo weather data.

> This is a demonstration project provided as-is for learning and testing purposes.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Features

This MCP server provides comprehensive access to Open-Meteo's weather APIs through 12 tools — 6 single-location tools and 6 batch tools for multi-location queries.

**All tools return fully-typed Pydantic v2 models** for type safety, validation, and excellent IDE support. Every model includes rich, LLM-friendly field descriptions with interpretation guides for better AI understanding.

### Single-Location Tools

#### 1. Weather Forecast (`get_weather_forecast`)
Get detailed weather forecasts with customizable parameters:
- Current weather conditions
- Hourly forecasts (up to 16 days)
- Daily forecasts
- 50+ weather variables including temperature, precipitation, wind, humidity, cloud cover, and more
- Multiple units (celsius/fahrenheit, km/h, mph, m/s, knots)
- Automatic timezone detection

#### 2. Location Geocoding (`geocode_location`)
Convert location names to coordinates:
- Search for any location worldwide
- Get coordinates, elevation, timezone
- Country and administrative information
- Population data where available
- Multi-language support

#### 3. Historical Weather (`get_historical_weather`)
Access historical weather data:
- Data from 1940 onwards (location-dependent)
- Same comprehensive variables as forecasts
- Perfect for climate analysis and trends
- Hourly and daily aggregations

#### 4. Air Quality (`get_air_quality`)
Monitor air quality and pollutants:
- PM2.5, PM10 particulate matter
- CO, NO2, SO2, O3 gas concentrations
- European AQI and US AQI indices
- Pollen data (multiple species)
- UV index
- Aerosol optical depth

#### 5. Marine Forecast (`get_marine_forecast`)
Get marine weather conditions:
- Wave height, direction, and period
- Wind waves and swell waves separately
- Ocean current velocity and direction
- Up to 16-day forecasts
- Essential for maritime activities
- Field descriptions include wave quality interpretations (0-0.5m calm, 1.5-2.5m moderate, etc.)

#### 6. Weather Code Interpretation (`interpret_weather_code`)
Translate numeric weather codes to descriptions:
- Converts WMO weather codes (0-99) to human-readable text
- Includes severity categories (clear, rain, snow, thunderstorm, etc.)
- Helps LLMs explain weather conditions in natural language
- Built-in reference for all standard weather codes

### Batch Tools

Batch tools dramatically reduce latency when querying multiple locations. Instead of N sequential tool calls (~3 minutes for 20 cities), batch tools complete in a single call (~0.3–0.5 seconds).

#### 7. Batch Geocoding (`batch_geocode_locations`)
Geocode multiple location names concurrently:
- Comma-separated input: `"London,Paris,Berlin,Madrid,Rome"`
- Concurrent execution with connection pooling
- Partial failure handling — individual locations can fail without breaking the batch
- Results in same order as input

#### 8. Batch Weather Forecasts (`batch_get_weather_forecasts`)
Fetch forecasts for up to 1000 locations in a single API call:
- Uses Open-Meteo's native multi-location support
- Single HTTP request for all locations
- Same parameters as `get_weather_forecast`

#### 9. Batch Air Quality (`batch_get_air_quality`)
Air quality data for multiple locations in one API call:
- Compare pollution levels across cities
- Defaults to common pollutant metrics (PM2.5, PM10, AQI, etc.)

#### 10. Batch Marine Forecasts (`batch_get_marine_forecasts`)
Marine conditions for multiple coastal points in one API call:
- Compare surf spots, monitor coastline conditions
- Waves, swell, currents, and tides across locations

#### 11. Batch Historical Weather (`batch_get_historical_weather`)
Historical data for multiple locations in one API call:
- All locations share the same date range
- Useful for climate comparisons across cities

#### 12. Batch Weather Code Interpretation (`batch_interpret_weather_codes`)
Interpret multiple WMO weather codes in a single call:
- Comma-separated input: `"3,51,61,95"`
- Eliminates multiple sequential `interpret_weather_code` calls
- Ideal after batch forecasts return different codes per location

### Recommended Batch Workflow

```
1. batch_geocode_locations("London,Paris,Berlin")  → coordinates
2. batch_get_weather_forecasts(latitudes="51.51,48.86,52.52", longitudes="-0.13,2.35,13.41")  → weather
3. batch_interpret_weather_codes("3,51,61")  → descriptions
```

## Installation

### Using uvx (Recommended - No Installation Required!)

The easiest way to use the server is with `uvx`, which runs it without installing:

```bash
uvx chuk-mcp-open-meteo
```

This automatically downloads and runs the latest version. Perfect for Claude Desktop!

### Using uv (Recommended for Development)

```bash
# Install from PyPI
uv pip install chuk-mcp-open-meteo

# Or clone and install from source
git clone <repository-url>
cd chuk-mcp-open-meteo
uv sync --dev
```

### Using pip (Traditional)

```bash
pip install chuk-mcp-open-meteo
```

## Usage

### With Claude Desktop

#### Option 1: Use the Public Server (Easiest)

Connect to the hosted public server at `weather.chukai.io`:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "url": "https://weather.chukai.io/mcp"
    }
  }
}
```

#### Option 2: Run Locally with uvx

```json
{
  "mcpServers": {
    "open-meteo": {
      "command": "uvx",
      "args": ["chuk-mcp-open-meteo"]
    }
  }
}
```

#### Option 3: Run Locally with pip

```json
{
  "mcpServers": {
    "open-meteo": {
      "command": "chuk-mcp-open-meteo"
    }
  }
}
```

### Standalone

Run the server directly:

```bash
# With uvx (recommended - always latest version)
uvx chuk-mcp-open-meteo

# With uvx in HTTP mode
uvx chuk-mcp-open-meteo http

# Or if installed locally
chuk-mcp-open-meteo
chuk-mcp-open-meteo http
```

Or with uv/Python:

```bash
# STDIO mode (default, for MCP clients)
uv run chuk-mcp-open-meteo
# or: python -m chuk_mcp_open_meteo.server

# HTTP mode (for web access)
uv run chuk-mcp-open-meteo http
# or: python -m chuk_mcp_open_meteo.server http
```

**STDIO mode** is for MCP clients like Claude Desktop and mcp-cli.
**HTTP mode** runs a web server on http://localhost:8000 for HTTP-based MCP clients.

## Example Usage

Once configured, you can ask Claude questions like:

- "What's the current weather in London?"
- "Give me a 7-day forecast for Tokyo with hourly temperature and precipitation"
- "What was the weather like in New York on July 4th, 2020?"
- "What's the air quality in Los Angeles right now?"
- "What are the wave conditions off the coast of Hawaii?"
- "Find the coordinates for Paris, France"

### Python Examples

Check out the `examples/` directory for runnable Python examples:

```bash
# With uv (recommended)
uv run python examples/example_basic.py
uv run python examples/example_trip_planner.py
uv run python examples/test_mcp_protocol.py

# Or with plain python (if installed)
python examples/example_basic.py
python examples/example_trip_planner.py
python examples/test_mcp_protocol.py

# Run all examples
./examples/test_all.sh
```

See [examples/README.md](examples/README.md) for detailed documentation.

## Tool Reference

All tools return **Pydantic v2 models** with full type safety. When calling from Python, you get clean object access:

```python
from chuk_mcp_open_meteo.server import get_weather_forecast

# Get weather forecast
forecast = await get_weather_forecast(latitude=51.5072, longitude=-0.1276, current_weather=True)

# Access data via typed attributes (not dictionaries!)
if forecast.current_weather:
    temp = forecast.current_weather.temperature  # Type-safe access
    wind = forecast.current_weather.windspeed
```

### get_weather_forecast

Parameters:
```python
{
  "latitude": 51.5072,
  "longitude": -0.1276,
  "temperature_unit": "celsius",  # or "fahrenheit"
  "wind_speed_unit": "kmh",       # or "ms", "mph", "kn"
  "precipitation_unit": "mm",      # or "inch"
  "timezone": "auto",              # or specific timezone
  "forecast_days": 7,              # 1-16
  "current_weather": true,
  "hourly": "temperature_2m,precipitation,wind_speed_10m",
  "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum"
}
```

Returns: `WeatherForecast` Pydantic model

**Popular hourly variables**: `temperature_2m`, `relative_humidity_2m`, `precipitation`, `rain`, `snowfall`, `cloud_cover`, `wind_speed_10m`, `wind_direction_10m`, `pressure_msl`, `visibility`

**Popular daily variables**: `temperature_2m_max`, `temperature_2m_min`, `precipitation_sum`, `rain_sum`, `sunrise`, `sunset`, `wind_speed_10m_max`

### geocode_location

Parameters:
```python
{
  "name": "London",
  "count": 10,        # number of results
  "language": "en"    # language code
}
```

Returns: `GeocodingResponse` Pydantic model

### get_historical_weather

Parameters:
```python
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "start_date": "2020-01-01",
  "end_date": "2020-01-31",
  "hourly": "temperature_2m,precipitation",
  "daily": "temperature_2m_max,temperature_2m_min"
}
```

Returns: `HistoricalWeather` Pydantic model

### get_air_quality

Parameters:
```python
{
  "latitude": 34.0522,
  "longitude": -118.2437,
  "hourly": "pm10,pm2_5,us_aqi,european_aqi"
}
```

Returns: `AirQualityResponse` Pydantic model

### get_marine_forecast

Parameters:
```python
{
  "latitude": 21.3099,
  "longitude": -157.8581,
  "hourly": "wave_height,wave_direction,wave_period"
}
```

Returns: `MarineForecast` Pydantic model

## Development

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd chuk-mcp-open-meteo

# Install with uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

### Running Tests

```bash
make test              # Run tests (excludes network tests)
make test-cov          # Run tests with coverage
make coverage-report   # Show coverage report

# Run all tests including network tests (requires internet)
pytest tests/          # Run all 40 tests
pytest tests/ -m network  # Run only network tests
```

**Note:** Network tests make real API calls to Open-Meteo and are excluded from CI to avoid flaky builds. They include automatic retry logic for local development.

### Code Quality

```bash
make lint      # Run linters
make format    # Auto-format code
make typecheck # Run type checking
make security  # Run security checks
make check     # Run all checks
```

### Building

```bash
make build         # Build package
make docker-build  # Build Docker image
```

## Deployment

### Fly.io

Deploy to Fly.io with a single command:

```bash
# First time setup
fly launch

# Deploy updates
fly deploy
```

The server will be available via HTTP at your Fly.io URL.

### Docker

```bash
# Build the image
docker build -t chuk-mcp-open-meteo .

# Run the container
docker run -p 8000:8000 chuk-mcp-open-meteo
```

## API Credits

This server uses the free [Open-Meteo API](https://open-meteo.com/). Open-Meteo provides:

- Free access for non-commercial use
- No API key required
- High-resolution weather models
- 25+ global weather models
- Historical data from 1940
- No rate limits for reasonable use

Please consider [supporting Open-Meteo](https://open-meteo.com/en/pricing) if you use this extensively.

## Architecture

Built on top of chuk-mcp-server, this server uses a modular architecture:

```
src/chuk_mcp_open_meteo/
├── server.py          # Thin entry point — imports tools, runs server
├── models.py          # All Pydantic v2 response models (26 models)
├── _constants.py      # API URLs, default parameters, weather codes
├── _batch.py          # Generic batch fetch helper (DRY across 4 batch tools)
└── tools/             # Domain-focused tool modules
    ├── forecast.py    # get_weather_forecast + batch_get_weather_forecasts
    ├── geocoding.py   # geocode_location + batch_geocode_locations
    ├── historical.py  # get_historical_weather + batch_get_historical_weather
    ├── air_quality.py # get_air_quality + batch_get_air_quality
    ├── marine.py      # get_marine_forecast + batch_get_marine_forecasts
    └── weather_codes.py # interpret_weather_code
```

Design principles:

- **Async Native**: All tools are async/await, all HTTP via httpx.AsyncClient
- **Pydantic Native**: All responses use Pydantic v2 models for validation and type safety
- **No Magic Strings**: API URLs and default parameters are named constants
- **Composable Modules**: Each domain is a self-contained module with single and batch tools
- **Type-Safe**: Automatic JSON-RPC schema generation from Python type hints
- **LLM-Optimized**: Rich field descriptions with interpretation guides embedded in models
  - Wave heights include size categories (calm/small/moderate/large/dangerous)
  - Wave periods include quality ratings (choppy/good/excellent)
  - Weather codes include quick reference in field descriptions
  - Direction fields explain meteorological conventions
  - All measurements include context and safety thresholds
- **High Performance**: Sub-3ms latency, 36,000+ RPS capability

## Public Server

A public instance is hosted at **weather.chukai.io** for easy access:

- **URL**: `https://weather.chukai.io/mcp`
- **Protocol**: MCP over HTTPS
- **Free to use**: No API key required
- **Always up-to-date**: Running the latest version

Simply add it to your Claude Desktop config:

```json
{
  "mcpServers": {
    "weather": {
      "url": "https://weather.chukai.io/mcp"
    }
  }
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for providing excellent free weather data
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [Anthropic](https://www.anthropic.com/) for Claude and MCP support

## License

Apache License 2.0 - See LICENSE for details.

## Documentation

- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
