# Examples

This directory contains runnable examples and tests for the Open-Meteo MCP Server.

## Python Examples

### Basic Usage (`example_basic.py`)

Demonstrates basic usage of the weather tools:
- Current weather lookup
- Location geocoding
- Weather forecasts
- Historical weather data
- Air quality information
- Marine forecasts

**Run it:**
```bash
python examples/example_basic.py
```

**Expected output:**
- Current weather in London
- Geocoding results for "Paris"
- 3-day forecast for Tokyo
- Historical weather for Paris (Jan 2024)
- Air quality in Los Angeles
- Marine conditions in Hawaii

### Trip Planner (`example_trip_planner.py`)

Advanced example showing how to combine multiple tools for real-world use cases.
Creates a comprehensive trip planning report with:
- Location lookup with timezone and elevation
- Multi-day weather forecast
- Current conditions
- Air quality assessment
- Packing recommendations based on weather

**Run it:**
```bash
python examples/example_trip_planner.py
```

**Plans trips to:**
- Rome, Italy (7 days)
- Tokyo, Japan (5 days)
- New York, USA (7 days)

**Customize it:**
```python
# In the script, modify the main() function:
await plan_trip("Barcelona, Spain", days=10)
await plan_trip("Sydney, Australia", days=5)
```

## MCP Protocol Tests

### Protocol Compliance Test (`test_mcp_protocol.py`)

Tests the MCP server implementation to ensure it correctly implements the Model Context Protocol.

**What it tests:**
1. Server initialization (handshake)
2. Tool listing (capabilities)
3. Tool invocation (get_weather_forecast)
4. Tool invocation (geocode_location)
5. Error handling (invalid tools, bad arguments)

**Run it:**
```bash
python examples/test_mcp_protocol.py
```

**Expected output:**
```
MCP PROTOCOL TESTS - chuk-mcp-open-meteo
=========================================

TEST: Server Initialization
✓ Initialization test passed

TEST: List Tools
✓ Found 12 tools
✓ List tools test passed

TEST: Call Weather Forecast Tool
✓ Weather forecast tool test passed

TEST: Call Geocode Location Tool
✓ Geocode tool test passed

TEST: Error Handling
✓ Error handling test passed

TEST SUMMARY
Passed: 5/5
✓ All tests passed! 🎉
```

## MCP CLI Testing

### Quick Test with MCP CLI

Test the server using `mcp-cli`:

```bash
# Install mcp-cli
pip install mcp-cli

# Run automated tests
./examples/test_with_mcp_cli.sh

# Interactive session
mcp-cli --server "python -m chuk_mcp_open_meteo.server" \
  --provider openai --model gpt-4o
```

See [MCP_CLI_TESTING.md](MCP_CLI_TESTING.md) for comprehensive testing guide.

### MCP Config File

Copy the example config to use with mcp-cli:

```bash
cp examples/mcp_config.json ~/.mcp/config.json

# Then use with
mcp-cli --server weather --provider openai --model gpt-4o
```

## Configuration Examples

### Claude Desktop Config (`claude_desktop_config.json`)

Standard installation using the installed package:
```json
{
  "mcpServers": {
    "open-meteo": {
      "command": "chuk-mcp-open-meteo"
    }
  }
}
```

**Location:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

### UV Installation (`claude_desktop_config_uv.json`)

Using UV's uvx runner:
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

### Development Mode

For testing during development:
```json
{
  "mcpServers": {
    "open-meteo": {
      "command": "python",
      "args": ["-m", "chuk_mcp_open_meteo.server"],
      "env": {
        "PYTHONPATH": "/path/to/chuk-mcp-open-meteo/src"
      }
    }
  }
}
```

## Running Examples

### Prerequisites

Install the package:
```bash
# From PyPI (when published)
pip install chuk-mcp-open-meteo

# From source (development)
cd /path/to/chuk-mcp-open-meteo
pip install -e .
```

### Run All Examples

```bash
# Basic examples
python examples/example_basic.py

# Trip planner
python examples/example_trip_planner.py

# MCP protocol tests
python examples/test_mcp_protocol.py
```

### Make Scripts Executable (Unix/macOS)

```bash
chmod +x examples/*.py
./examples/example_basic.py
./examples/example_trip_planner.py
./examples/test_mcp_protocol.py
```

## Creating Your Own Examples

### Template

```python
#!/usr/bin/env python3
"""Your example description."""

import asyncio
from chuk_mcp_open_meteo.server import (
    get_weather_forecast,
    geocode_location,
    # ... other tools
)


async def main():
    """Your main function."""

    # 1. Geocode your location
    location = await geocode_location(name="Your City")
    lat = location["results"][0]["latitude"]
    lon = location["results"][0]["longitude"]

    # 2. Get weather
    weather = await get_weather_forecast(
        latitude=lat,
        longitude=lon,
        current_weather=True,
    )

    # 3. Do something with the data
    print(f"Temperature: {weather['current_weather']['temperature']}°C")


if __name__ == "__main__":
    asyncio.run(main())
```

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError: No module named 'chuk_mcp_open_meteo'`:

```bash
# Make sure the package is installed
pip install -e .

# Or set PYTHONPATH
export PYTHONPATH=/path/to/chuk-mcp-open-meteo/src:$PYTHONPATH
python examples/example_basic.py
```

### API Errors

If you get HTTP errors or timeouts:
- Check your internet connection
- Open-Meteo API may be temporarily unavailable
- Try again in a few moments

### MCP Protocol Test Failures

If `test_mcp_protocol.py` fails:
- Ensure chuk-mcp-server is installed: `pip install chuk-mcp-server`
- Check that the server starts correctly: `python -m chuk_mcp_open_meteo.server`
- Review error messages for specific issues

## Additional Resources

- [Full Documentation](../README.md)
- [Usage Examples](usage_examples.md) - Comprehensive examples with Claude
- [Contributing Guide](../CONTRIBUTING.md)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs)

## Example Ideas

Want to create more examples? Here are some ideas:

1. **Weather Comparison Tool** - Compare weather across multiple cities
2. **Climate Analyzer** - Analyze historical trends over years
3. **Outdoor Activity Planner** - Best times for hiking, biking, etc.
4. **Agriculture Helper** - Precipitation and temperature analysis for farming
5. **Event Planner** - Weather risk assessment for outdoor events
6. **Health Monitor** - Air quality and pollen tracking for health conditions
7. **Marine Activity Planner** - Surfing, sailing, fishing conditions
8. **Weather Alert System** - Monitor conditions and send notifications
9. **Climate Change Tracker** - Long-term temperature trend analysis
10. **Smart Home Integration** - Weather-based automation triggers

Feel free to contribute your own examples via pull request!
