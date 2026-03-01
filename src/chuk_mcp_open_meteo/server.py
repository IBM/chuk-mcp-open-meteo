"""Open-Meteo MCP Server — entry point.

Imports tool modules to register @tool decorators, then runs the server.
"""

import logging
import sys

from chuk_mcp_server import run

# Import the tools package — this triggers @tool registration for all tools.
from . import tools  # noqa: F401

# Re-export tool functions so existing imports (e.g. tests, scripts) keep working.
from .tools.air_quality import batch_get_air_quality, get_air_quality
from .tools.forecast import batch_get_weather_forecasts, get_weather_forecast
from .tools.geocoding import batch_geocode_locations, geocode_location
from .tools.historical import batch_get_historical_weather, get_historical_weather
from .tools.marine import batch_get_marine_forecasts, get_marine_forecast
from .tools.weather_codes import batch_interpret_weather_codes, interpret_weather_code

# Configure logging
# In STDIO mode, we need to be quiet to avoid polluting the JSON-RPC stream
# Only log to stderr, and only warnings/errors
logging.basicConfig(
    level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s", stream=sys.stderr
)
logger = logging.getLogger(__name__)

__all__ = [
    "batch_geocode_locations",
    "batch_get_air_quality",
    "batch_get_historical_weather",
    "batch_get_marine_forecasts",
    "batch_get_weather_forecasts",
    "batch_interpret_weather_codes",
    "geocode_location",
    "get_air_quality",
    "get_historical_weather",
    "get_marine_forecast",
    "get_weather_forecast",
    "interpret_weather_code",
    "main",
]


def main():
    """Run the Open-Meteo MCP server."""
    # Check if transport is specified in command line args
    # Default to stdio for MCP compatibility (Claude Desktop, mcp-cli)
    transport = "stdio"

    # Allow HTTP mode via command line
    if len(sys.argv) > 1 and sys.argv[1] in ["http", "--http"]:
        transport = "http"
        # Only log in HTTP mode
        logger.warning("Starting Chuk MCP Open-Meteo Server in HTTP mode")

    # Suppress chuk_mcp_server logging in STDIO mode
    if transport == "stdio":
        # Set chuk_mcp_server loggers to ERROR only
        logging.getLogger("chuk_mcp_server").setLevel(logging.ERROR)
        logging.getLogger("chuk_mcp_server.core").setLevel(logging.ERROR)
        logging.getLogger("chuk_mcp_server.stdio_transport").setLevel(logging.ERROR)
        # Suppress httpx logging (API calls)
        logging.getLogger("httpx").setLevel(logging.ERROR)

    run(transport=transport)


if __name__ == "__main__":
    main()
