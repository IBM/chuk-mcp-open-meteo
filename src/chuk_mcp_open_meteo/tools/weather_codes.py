"""Weather code interpretation tools."""

from chuk_mcp_server import tool

from .._constants import WEATHER_CODES
from ..models import (
    BatchWeatherCodeItem,
    BatchWeatherCodeResponse,
    WeatherCodeInterpretation,
)


@tool
async def interpret_weather_code(weather_code: int) -> WeatherCodeInterpretation:
    """Interpret WMO weather codes used by Open-Meteo API.

    Weather codes are numerical values (0-99) that represent different weather conditions.
    This tool translates codes into human-readable descriptions.

    Args:
        weather_code: WMO weather code integer (0-99) from weather forecast data.
            This is the 'weathercode' field in current_weather or hourly/daily data.

    Returns:
        WeatherCodeInterpretation: Pydantic model with:
            - code: The weather code number
            - description: Human-readable weather condition
            - severity: Category (clear, cloudy, fog, drizzle, rain, freezing, snow, showers, thunderstorm)

    Common Weather Codes:
        Clear/Cloudy (0-3):
            0 = Clear sky
            1 = Mainly clear
            2 = Partly cloudy
            3 = Overcast

        Fog (45-48):
            45 = Fog
            48 = Depositing rime fog

        Drizzle (51-57):
            51 = Light drizzle
            53 = Moderate drizzle
            55 = Dense drizzle
            56-57 = Freezing drizzle

        Rain (61-67):
            61 = Slight rain
            63 = Moderate rain
            65 = Heavy rain
            66-67 = Freezing rain

        Snow (71-77, 85-86):
            71 = Slight snow
            73 = Moderate snow
            75 = Heavy snow
            77 = Snow grains
            85-86 = Snow showers

        Showers (80-82):
            80 = Slight rain showers
            81 = Moderate rain showers
            82 = Violent rain showers

        Thunderstorm (95-99):
            95 = Thunderstorm
            96 = Thunderstorm with slight hail
            99 = Thunderstorm with heavy hail

    Tips for LLMs:
        - Use this to explain weather conditions to users in natural language
        - Severity helps determine appropriate activity recommendations
        - Codes 0-3: Generally safe outdoor conditions
        - Codes 51-65: Wet conditions, bring umbrella
        - Codes 71-77: Snow conditions, winter gear needed
        - Codes 80-99: Severe weather, take precautions
        - Unknown codes return "Unknown weather code" - may be API error

    Example:
        # Get weather and interpret code
        forecast = await get_weather_forecast(lat, lon, current_weather=True)
        code = forecast.current_weather.weathercode
        interpretation = await interpret_weather_code(code)
        # Returns: WeatherCodeInterpretation(code=61, description="Slight rain", severity="rain")
    """
    if weather_code in WEATHER_CODES:
        return WeatherCodeInterpretation(
            code=weather_code,
            description=WEATHER_CODES[weather_code]["description"],
            severity=WEATHER_CODES[weather_code]["severity"],
        )
    else:
        return WeatherCodeInterpretation(
            code=weather_code,
            description=f"Unknown weather code: {weather_code}",
            severity="unknown",
        )


@tool
async def batch_interpret_weather_codes(weather_codes: str) -> BatchWeatherCodeResponse:
    """Interpret multiple WMO weather codes in a single call.

    Instead of calling interpret_weather_code multiple times (one per code),
    pass all codes at once. This is much more efficient when processing
    weather data for multiple locations.

    Args:
        weather_codes: Comma-separated WMO weather code integers (0-99).
            Example: "3,51,61,95" or "0, 3, 45, 80"

    Returns:
        BatchWeatherCodeResponse: Pydantic model with:
            - results: List of interpretations in same order as input
            - total_codes: Number of codes processed

    Example:
        # After batch forecast returns codes for multiple cities:
        result = await batch_interpret_weather_codes("3,51,61,95")
        # Returns all interpretations in one call instead of 4 separate calls
    """
    codes = [c.strip() for c in weather_codes.split(",") if c.strip()]

    items = []
    for code_str in codes:
        try:
            code = int(code_str)
        except ValueError:
            items.append(
                BatchWeatherCodeItem(
                    code=-1,
                    description=f"Invalid weather code: {code_str!r}",
                    severity="unknown",
                )
            )
            continue

        if code in WEATHER_CODES:
            items.append(
                BatchWeatherCodeItem(
                    code=code,
                    description=WEATHER_CODES[code]["description"],
                    severity=WEATHER_CODES[code]["severity"],
                )
            )
        else:
            items.append(
                BatchWeatherCodeItem(
                    code=code,
                    description=f"Unknown weather code: {code}",
                    severity="unknown",
                )
            )

    return BatchWeatherCodeResponse(results=items, total_codes=len(items))
