# Testing with MCP CLI

This guide shows how to test the Open-Meteo MCP server using the `mcp-cli` tool.

## Prerequisites

Install mcp-cli:
```bash
pip install mcp-cli
# or
uvx mcp-cli
```

## Configuration

### Option 1: Using MCP Config File

Create or edit `~/.mcp/config.json`:

```json
{
  "servers": {
    "weather": {
      "command": "chuk-mcp-open-meteo",
      "type": "stdio"
    }
  }
}
```

Or for development:

```json
{
  "servers": {
    "weather": {
      "command": "python",
      "args": ["-m", "chuk_mcp_open_meteo.server"],
      "env": {
        "PYTHONPATH": "/path/to/chuk-mcp-open-meteo/src"
      },
      "type": "stdio"
    }
  }
}
```

### Option 2: Command Line

Test directly without config:

```bash
mcp-cli --server "python -m chuk_mcp_open_meteo.server" --provider openai --model gpt-4
```

## Testing Commands

### 1. List Available Tools

```bash
mcp-cli --server weather tools
```

**Expected output:**
```
Available tools from weather:
  - get_weather_forecast: Get comprehensive weather forecast from Open-Meteo API
  - geocode_location: Search for locations and get their coordinates
  - get_historical_weather: Get historical weather data from Open-Meteo Archive API
  - get_air_quality: Get air quality data and forecasts
  - get_marine_forecast: Get marine weather forecast
  - interpret_weather_code: Interpret WMO weather codes
  - batch_geocode_locations: Geocode multiple locations concurrently
  - batch_get_weather_forecasts: Fetch forecasts for multiple locations
  - batch_get_air_quality: Air quality for multiple locations
  - batch_get_marine_forecasts: Marine conditions for multiple locations
  - batch_get_historical_weather: Historical data for multiple locations
  - batch_interpret_weather_codes: Interpret multiple weather codes at once
```

### 2. Start Interactive Chat

```bash
mcp-cli --server weather --provider openai --model gpt-4o
```

Or with a local model:

```bash
mcp-cli --server weather --provider ollama --model llama3.2
```

### 3. Test Specific Queries

#### Current Weather
```
> What's the current weather in London?
```

The assistant should:
1. Use `geocode_location` to find London
2. Use `get_weather_forecast` with the coordinates
3. Return formatted weather data

#### Multi-day Forecast
```
> Give me a 5-day forecast for Tokyo with temperature and precipitation
```

#### Historical Weather
```
> What was the weather like in Paris on January 1st, 2024?
```

#### Air Quality
```
> What's the air quality in Los Angeles right now?
```

#### Marine Forecast
```
> What are the wave conditions off the coast of Hawaii?
```

#### Complex Query
```
> I'm planning a trip to Rome next week. Should I pack an umbrella?
What's the weather forecast and air quality like?
```

The assistant should:
1. Geocode Rome
2. Get weather forecast
3. Get air quality
4. Analyze and provide recommendations

## Testing Individual Tools

### Test Weather Forecast

```bash
mcp-cli --server weather cmd call-tool \
  --name get_weather_forecast \
  --params '{"latitude": 51.5072, "longitude": -0.1276, "current_weather": true}'
```

### Test Geocoding

```bash
mcp-cli --server weather cmd call-tool \
  --name geocode_location \
  --params '{"name": "Paris", "count": 3}'
```

### Test Historical Weather

```bash
mcp-cli --server weather cmd call-tool \
  --name get_historical_weather \
  --params '{
    "latitude": 48.8566,
    "longitude": 2.3522,
    "start_date": "2024-01-01",
    "end_date": "2024-01-07",
    "daily": "temperature_2m_max,temperature_2m_min"
  }'
```

### Test Air Quality

```bash
mcp-cli --server weather cmd call-tool \
  --name get_air_quality \
  --params '{"latitude": 34.0522, "longitude": -118.2437}'
```

### Test Marine Forecast

```bash
mcp-cli --server weather cmd call-tool \
  --name get_marine_forecast \
  --params '{"latitude": 21.3099, "longitude": -157.8581}'
```

## Debugging

### Verbose Mode

Enable verbose logging:

```bash
mcp-cli --server weather --provider openai --model gpt-4 --verbose
```

This shows:
- Protocol handshake
- Tool discovery
- Tool calls and responses
- Error messages

### Check Server Status

```bash
# Ping the server
mcp-cli --server weather ping

# List resources
mcp-cli --server weather resources

# List prompts
mcp-cli --server weather prompts
```

### Test Server Directly

Test the server binary directly:

```bash
# Run the server
python -m chuk_mcp_open_meteo.server

# It should start and wait for JSON-RPC messages on stdin
# Send test message (Ctrl+C to exit):
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05"}}
```

## Common Issues

### Server Not Found

**Error:** `Server 'weather' not found`

**Solution:**
1. Check config file exists: `cat ~/.mcp/config.json`
2. Verify server name matches config
3. Try full command: `mcp-cli --server "chuk-mcp-open-meteo"`

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'chuk_mcp_open_meteo'`

**Solution:**
```bash
# Install the package
pip install chuk-mcp-open-meteo

# Or in development mode
cd /path/to/chuk-mcp-open-meteo
pip install -e .
```

### Tool Call Failures

**Error:** `HTTPError: 404 Not Found`

**Solution:**
- Check internet connection
- Verify coordinates are valid (latitude: -90 to 90, longitude: -180 to 180)
- Check date format for historical queries (YYYY-MM-DD)

### Provider/Model Issues

**Error:** `Provider 'openai' not configured`

**Solution:**
```bash
# Set OpenAI API key
export OPENAI_API_KEY=sk-...

# Or use a local model
mcp-cli --server weather --provider ollama --model llama3.2
```

## Example Session

Here's a complete testing session:

```bash
# 1. Start the CLI
mcp-cli --server weather --provider openai --model gpt-4o

# 2. Test basic query
> What's the weather in London?

# Expected: Assistant uses geocode_location, then get_weather_forecast
# and returns current conditions

# 3. Test forecast
> Give me a 3-day forecast for Tokyo

# Expected: Returns temperature, precipitation for 3 days

# 4. Test historical
> What was the weather in Paris on January 15, 2024?

# Expected: Uses historical API, returns past weather

# 5. Test air quality
> Is the air quality good in Los Angeles?

# Expected: Returns AQI and health recommendations

# 6. Test complex query
> I'm going surfing in Hawaii tomorrow. What are the conditions?

# Expected: Uses both weather and marine forecasts
# Returns wave height, wind, weather

# 7. Exit
> exit
```

## Performance Testing

### Measure Response Time

```bash
time mcp-cli --server weather cmd call-tool \
  --name get_weather_forecast \
  --params '{"latitude": 51.5072, "longitude": -0.1276, "current_weather": true}'
```

### Concurrent Requests

Test multiple tools in one query:

```
> For London, I need: current weather, 7-day forecast, air quality,
  and historical weather for last week
```

The assistant should efficiently call multiple tools.

## Advanced Testing

### Custom Weather Variables

```
> Get hourly forecast for New York for tomorrow including temperature,
  precipitation, wind speed, humidity, and cloud cover
```

### Multiple Locations

```
> Compare the weather in London, Paris, and Berlin for this weekend
```

### Climate Analysis

```
> Compare average temperatures in New York between January 2023 and January 2024
```

## Automated Testing Script

Create a test script `test_mcp_cli.sh`:

```bash
#!/bin/bash

echo "Testing Open-Meteo MCP Server with mcp-cli"
echo "=========================================="

# Test 1: List tools
echo "Test 1: Listing tools..."
mcp-cli --server weather tools

# Test 2: Weather forecast
echo "Test 2: Weather forecast..."
mcp-cli --server weather cmd call-tool \
  --name get_weather_forecast \
  --params '{"latitude": 51.5072, "longitude": -0.1276, "current_weather": true}'

# Test 3: Geocoding
echo "Test 3: Geocoding..."
mcp-cli --server weather cmd call-tool \
  --name geocode_location \
  --params '{"name": "Paris", "count": 1}'

echo "All tests completed!"
```

Make executable and run:
```bash
chmod +x test_mcp_cli.sh
./test_mcp_cli.sh
```

## Integration with Other Tools

### Use with LangChain

```python
from langchain.tools import Tool
from chuk_mcp_open_meteo.server import get_weather_forecast

weather_tool = Tool(
    name="weather",
    description="Get weather forecast",
    func=lambda args: get_weather_forecast(**args)
)
```

### Use with AutoGen

```python
from autogen import AssistantAgent

assistant = AssistantAgent(
    name="weather_assistant",
    mcp_servers=["weather"]
)
```

## Tips for Best Results

1. **Be Specific**: Include location names, not just coordinates
2. **Use Natural Language**: The AI will handle tool selection
3. **Combine Queries**: Ask for multiple data points in one question
4. **Specify Units**: Mention if you want Fahrenheit, mph, etc.
5. **Date Formats**: Use YYYY-MM-DD for historical queries

## Further Reading

- [MCP CLI Documentation](https://github.com/anthropics/mcp-cli)
- [Open-Meteo API Docs](https://open-meteo.com/en/docs)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Examples](./README.md)
