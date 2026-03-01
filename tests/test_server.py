"""Tests for the Open-Meteo MCP server with Pydantic models."""

import pytest

from chuk_mcp_open_meteo.models import (
    AirQualityResponse,
    BatchAirQualityResponse,
    BatchGeocodingResponse,
    BatchHistoricalWeatherResponse,
    BatchMarineForecastResponse,
    BatchWeatherCodeResponse,
    BatchWeatherForecastResponse,
    GeocodingResponse,
    HistoricalWeather,
    MarineForecast,
    WeatherForecast,
)
from chuk_mcp_open_meteo.server import (
    batch_geocode_locations,
    batch_get_air_quality,
    batch_get_historical_weather,
    batch_get_marine_forecasts,
    batch_get_weather_forecasts,
    batch_interpret_weather_codes,
    get_air_quality,
    geocode_location,
    get_historical_weather,
    get_marine_forecast,
    get_weather_forecast,
)


@pytest.mark.asyncio
async def test_get_weather_forecast():
    """Test getting weather forecast for London."""
    result = await get_weather_forecast(
        latitude=51.5072,
        longitude=-0.1276,
        current_weather=True,
    )

    assert isinstance(result, WeatherForecast)
    assert result.latitude == pytest.approx(51.5072, abs=0.1)
    assert result.longitude == pytest.approx(-0.1276, abs=0.1)
    assert result.current_weather is not None
    assert result.current_weather.temperature is not None


@pytest.mark.asyncio
async def test_get_weather_forecast_with_hourly():
    """Test getting weather forecast with hourly data."""
    result = await get_weather_forecast(
        latitude=40.7128,
        longitude=-74.0060,
        hourly="temperature_2m,precipitation",
        forecast_days=3,
    )

    assert isinstance(result, WeatherForecast)
    assert result.hourly is not None
    assert result.hourly.temperature_2m is not None
    assert result.hourly.precipitation is not None


@pytest.mark.asyncio
async def test_geocode_location():
    """Test geocoding a location."""
    result = await geocode_location(name="London", count=5)

    assert isinstance(result, GeocodingResponse)
    assert result.results is not None
    assert len(result.results) > 0

    # First result should be London, UK
    london = result.results[0]
    assert london.name is not None
    assert london.latitude is not None
    assert london.longitude is not None
    assert london.country is not None


@pytest.mark.asyncio
async def test_geocode_multiple_results():
    """Test geocoding returns multiple results for ambiguous names."""
    result = await geocode_location(name="Paris", count=10)

    assert isinstance(result, GeocodingResponse)
    assert result.results is not None
    # Should find Paris, France and Paris, Texas at minimum
    assert len(result.results) >= 2


@pytest.mark.asyncio
async def test_get_historical_weather():
    """Test getting historical weather data."""
    result = await get_historical_weather(
        latitude=48.8566,
        longitude=2.3522,
        start_date="2024-01-01",
        end_date="2024-01-07",
        daily="temperature_2m_max,temperature_2m_min",
    )

    assert isinstance(result, HistoricalWeather)
    assert result.latitude == pytest.approx(48.8566, abs=0.1)
    assert result.daily is not None
    assert result.daily.temperature_2m_max is not None
    assert result.daily.temperature_2m_min is not None


@pytest.mark.asyncio
async def test_get_air_quality():
    """Test getting air quality data."""
    result = await get_air_quality(
        latitude=34.0522,
        longitude=-118.2437,
    )

    assert isinstance(result, AirQualityResponse)
    assert result.latitude == pytest.approx(34.0522, abs=0.1)
    assert result.hourly is not None
    # Should have default air quality metrics
    assert result.hourly.pm10 is not None or result.hourly.pm2_5 is not None


@pytest.mark.asyncio
async def test_get_marine_forecast():
    """Test getting marine forecast."""
    result = await get_marine_forecast(
        latitude=21.3099,
        longitude=-157.8581,
    )

    assert isinstance(result, MarineForecast)
    assert result.latitude == pytest.approx(21.3099, abs=0.1)
    assert result.hourly is not None
    # Should have default marine metrics
    assert result.hourly.wave_height is not None


@pytest.mark.asyncio
async def test_weather_forecast_units():
    """Test weather forecast with different units."""
    result = await get_weather_forecast(
        latitude=25.7617,
        longitude=-80.1918,
        temperature_unit="fahrenheit",
        wind_speed_unit="mph",
        precipitation_unit="inch",
        current_weather=True,
    )

    assert isinstance(result, WeatherForecast)
    assert result.current_weather is not None
    # Temperature should be in reasonable Fahrenheit range
    temp = result.current_weather.temperature
    assert -50 <= temp <= 150  # Reasonable Fahrenheit range


@pytest.mark.asyncio
async def test_weather_forecast_timezone():
    """Test weather forecast with specific timezone."""
    result = await get_weather_forecast(
        latitude=35.6762,
        longitude=139.6503,
        timezone="Asia/Tokyo",
        current_weather=True,
    )

    assert isinstance(result, WeatherForecast)
    assert result.timezone == "Asia/Tokyo"


@pytest.mark.asyncio
async def test_historical_weather_hourly():
    """Test historical weather with hourly data."""
    result = await get_historical_weather(
        latitude=37.7749,
        longitude=-122.4194,
        start_date="2024-06-01",
        end_date="2024-06-02",
        hourly="temperature_2m,precipitation",
    )

    assert isinstance(result, HistoricalWeather)
    assert result.hourly is not None
    assert result.hourly.temperature_2m is not None
    assert result.hourly.time is not None
    # Should have 24 hours of data for 2 days
    assert len(result.hourly.time) >= 24


@pytest.mark.asyncio
async def test_marine_forecast_detailed():
    """Test marine forecast with detailed parameters."""
    result = await get_marine_forecast(
        latitude=0,  # Equator
        longitude=0,  # Prime meridian
        hourly="wave_height,wave_direction,wave_period,ocean_current_velocity",
        forecast_days=3,
    )

    assert isinstance(result, MarineForecast)
    assert result.hourly is not None
    assert result.hourly.wave_height is not None
    assert result.hourly.wave_direction is not None
    assert result.hourly.wave_period is not None


def test_imports():
    """Test that all tools and models can be imported."""
    from chuk_mcp_open_meteo import server
    from chuk_mcp_open_meteo import models

    assert hasattr(server, "get_weather_forecast")
    assert hasattr(server, "geocode_location")
    assert hasattr(server, "get_historical_weather")
    assert hasattr(server, "get_air_quality")
    assert hasattr(server, "get_marine_forecast")

    assert hasattr(models, "WeatherForecast")
    assert hasattr(models, "GeocodingResponse")
    assert hasattr(models, "HistoricalWeather")
    assert hasattr(models, "AirQualityResponse")
    assert hasattr(models, "MarineForecast")


@pytest.mark.asyncio
@pytest.mark.network
async def test_pydantic_validation(retry_on_network_error):
    """Test that Pydantic validation works correctly."""
    result = await retry_on_network_error(
        lambda: get_weather_forecast(
            latitude=51.5072,
            longitude=-0.1276,
            current_weather=True,
        )
    )

    # Pydantic models should have dict() method
    assert hasattr(result, "model_dump")
    data = result.model_dump()
    assert isinstance(data, dict)
    assert "latitude" in data
    assert "longitude" in data


@pytest.mark.asyncio
@pytest.mark.network
async def test_nested_model_access(retry_on_network_error):
    """Test accessing nested Pydantic models."""
    result = await retry_on_network_error(
        lambda: get_weather_forecast(
            latitude=51.5072,
            longitude=-0.1276,
            current_weather=True,
        )
    )

    # Test nested model access
    assert result.current_weather is not None
    assert hasattr(result.current_weather, "temperature")
    assert hasattr(result.current_weather, "windspeed")
    assert hasattr(result.current_weather, "winddirection")

    # Should be able to access via dot notation
    temp = result.current_weather.temperature
    assert isinstance(temp, (int, float))


@pytest.mark.asyncio
@pytest.mark.network
async def test_weather_forecast_with_daily(retry_on_network_error):
    """Test weather forecast with daily data."""
    result = await retry_on_network_error(
        lambda: get_weather_forecast(
            latitude=40.7128,
            longitude=-74.0060,
            daily="temperature_2m_max,temperature_2m_min,precipitation_sum",
            forecast_days=3,
        )
    )

    assert isinstance(result, WeatherForecast)
    assert result.daily is not None
    assert result.daily.temperature_2m_max is not None
    assert result.daily.temperature_2m_min is not None


@pytest.mark.asyncio
@pytest.mark.network
async def test_air_quality_with_custom_hourly(retry_on_network_error):
    """Test air quality with custom hourly parameters."""
    result = await retry_on_network_error(
        lambda: get_air_quality(
            latitude=34.0522,
            longitude=-118.2437,
            hourly="pm10,ozone,us_aqi",
        )
    )

    assert isinstance(result, AirQualityResponse)
    assert result.hourly is not None
    assert result.hourly.pm10 is not None


@pytest.mark.asyncio
@pytest.mark.network
async def test_marine_forecast_with_daily(retry_on_network_error):
    """Test marine forecast with daily data."""
    result = await retry_on_network_error(
        lambda: get_marine_forecast(
            latitude=21.3099,
            longitude=-157.8581,
            daily="wave_height_max,wave_direction_dominant",
            forecast_days=3,
        )
    )

    assert isinstance(result, MarineForecast)
    assert result.daily is not None
    assert result.daily.wave_height_max is not None


def test_main_function_stdio():
    """Test that main function sets up logging correctly for stdio mode."""
    import sys
    import logging
    from unittest.mock import patch

    # Save original argv
    original_argv = sys.argv.copy()

    try:
        # Test stdio mode (default)
        sys.argv = ["chuk-mcp-open-meteo"]

        with patch("chuk_mcp_open_meteo.server.run") as mock_run:
            from chuk_mcp_open_meteo.server import main

            main()

            # Verify run was called with stdio transport
            mock_run.assert_called_once_with(transport="stdio")

            # Verify logging was configured for stdio mode
            assert logging.getLogger("chuk_mcp_server").level == logging.ERROR
            assert logging.getLogger("httpx").level == logging.ERROR

    finally:
        # Restore original argv
        sys.argv = original_argv


def test_main_function_http():
    """Test that main function sets up http mode correctly."""
    import sys
    from unittest.mock import patch

    # Save original argv
    original_argv = sys.argv.copy()

    try:
        # Test http mode
        sys.argv = ["chuk-mcp-open-meteo", "http"]

        with patch("chuk_mcp_open_meteo.server.run") as mock_run:
            from chuk_mcp_open_meteo.server import main

            main()

            # Verify run was called with http transport
            mock_run.assert_called_once_with(transport="http")

    finally:
        # Restore original argv
        sys.argv = original_argv


# --- Batch Tool Tests ---


@pytest.mark.asyncio
async def test_batch_geocode_locations_basic():
    """Test batch geocoding with multiple cities."""
    result = await batch_geocode_locations(names="London,Paris,Berlin")

    assert isinstance(result, BatchGeocodingResponse)
    assert result.total_queries == 3
    assert result.successful >= 2
    assert len(result.results) == 3
    # Verify order preserved
    assert result.results[0].query == "London"
    assert result.results[1].query == "Paris"
    assert result.results[2].query == "Berlin"
    # Verify found items have coordinates
    for item in result.results:
        if item.found:
            assert item.results is not None
            assert len(item.results) > 0
            assert item.results[0].latitude is not None
            assert item.results[0].longitude is not None


@pytest.mark.asyncio
async def test_batch_geocode_locations_empty():
    """Test batch geocoding with empty input."""
    result = await batch_geocode_locations(names="")

    assert isinstance(result, BatchGeocodingResponse)
    assert result.total_queries == 0
    assert result.successful == 0
    assert result.failed == 0
    assert len(result.results) == 0


@pytest.mark.asyncio
async def test_batch_geocode_locations_partial_failure():
    """Test batch geocoding where some locations are not found."""
    result = await batch_geocode_locations(names="London,XyzNotARealPlace12345,Paris")

    assert isinstance(result, BatchGeocodingResponse)
    assert result.total_queries == 3
    # London and Paris should be found
    assert result.results[0].query == "London"
    assert result.results[2].query == "Paris"
    # The nonsense name
    nonsense_item = result.results[1]
    assert nonsense_item.query == "XyzNotARealPlace12345"
    assert nonsense_item.found is False


@pytest.mark.asyncio
async def test_batch_geocode_locations_whitespace():
    """Test that whitespace around commas is trimmed."""
    result = await batch_geocode_locations(names="London , Paris , Berlin")

    assert isinstance(result, BatchGeocodingResponse)
    assert result.total_queries == 3
    assert result.results[0].query == "London"
    assert result.results[1].query == "Paris"
    assert result.results[2].query == "Berlin"


@pytest.mark.asyncio
async def test_batch_get_weather_forecasts_basic():
    """Test batch weather forecasts for multiple locations."""
    # London, Paris, Berlin
    result = await batch_get_weather_forecasts(
        latitudes="51.51,48.86,52.52",
        longitudes="-0.13,2.35,13.41",
        current_weather=True,
    )

    assert isinstance(result, BatchWeatherForecastResponse)
    assert result.total_locations == 3
    assert len(result.results) == 3
    for i, item in enumerate(result.results):
        assert item.location_index == i
        assert item.forecast.current_weather is not None
        assert item.forecast.current_weather.temperature is not None


@pytest.mark.asyncio
async def test_batch_get_weather_forecasts_single():
    """Test batch forecast with single location (edge case)."""
    result = await batch_get_weather_forecasts(
        latitudes="51.51",
        longitudes="-0.13",
        current_weather=True,
    )

    assert isinstance(result, BatchWeatherForecastResponse)
    assert result.total_locations == 1
    assert len(result.results) == 1
    assert result.results[0].location_index == 0


@pytest.mark.asyncio
async def test_batch_get_weather_forecasts_with_daily():
    """Test batch forecast with daily parameters."""
    result = await batch_get_weather_forecasts(
        latitudes="51.51,48.86",
        longitudes="-0.13,2.35",
        daily="temperature_2m_max,temperature_2m_min",
        forecast_days=3,
    )

    assert isinstance(result, BatchWeatherForecastResponse)
    assert result.total_locations == 2
    for item in result.results:
        assert item.forecast.daily is not None
        assert item.forecast.daily.temperature_2m_max is not None


def test_batch_imports():
    """Test that batch tools and models can be imported."""
    from chuk_mcp_open_meteo import server
    from chuk_mcp_open_meteo import models

    assert hasattr(server, "batch_geocode_locations")
    assert hasattr(server, "batch_get_weather_forecasts")
    assert hasattr(server, "batch_get_air_quality")
    assert hasattr(server, "batch_get_marine_forecasts")
    assert hasattr(server, "batch_get_historical_weather")
    assert hasattr(server, "batch_interpret_weather_codes")

    assert hasattr(models, "BatchGeocodingResponse")
    assert hasattr(models, "BatchGeocodingItem")
    assert hasattr(models, "BatchWeatherForecastResponse")
    assert hasattr(models, "BatchWeatherForecastItem")
    assert hasattr(models, "BatchAirQualityResponse")
    assert hasattr(models, "BatchAirQualityItem")
    assert hasattr(models, "BatchMarineForecastResponse")
    assert hasattr(models, "BatchMarineForecastItem")
    assert hasattr(models, "BatchHistoricalWeatherResponse")
    assert hasattr(models, "BatchHistoricalWeatherItem")
    assert hasattr(models, "BatchWeatherCodeResponse")
    assert hasattr(models, "BatchWeatherCodeItem")


# --- Batch Air Quality Tests ---


@pytest.mark.asyncio
async def test_batch_get_air_quality_basic():
    """Test batch air quality for multiple locations."""
    # London, Paris, Berlin
    result = await batch_get_air_quality(
        latitudes="51.51,48.86,52.52",
        longitudes="-0.13,2.35,13.41",
    )

    assert isinstance(result, BatchAirQualityResponse)
    assert result.total_locations == 3
    assert len(result.results) == 3
    for i, item in enumerate(result.results):
        assert item.location_index == i
        assert item.air_quality.hourly is not None


@pytest.mark.asyncio
async def test_batch_get_air_quality_single():
    """Test batch air quality with single location."""
    result = await batch_get_air_quality(
        latitudes="34.05",
        longitudes="-118.24",
    )

    assert isinstance(result, BatchAirQualityResponse)
    assert result.total_locations == 1
    assert len(result.results) == 1
    assert result.results[0].location_index == 0
    assert result.results[0].air_quality.hourly is not None


@pytest.mark.asyncio
async def test_batch_get_air_quality_custom_hourly():
    """Test batch air quality with custom hourly variables."""
    result = await batch_get_air_quality(
        latitudes="51.51,48.86",
        longitudes="-0.13,2.35",
        hourly="pm2_5,us_aqi",
    )

    assert isinstance(result, BatchAirQualityResponse)
    assert result.total_locations == 2
    for item in result.results:
        assert item.air_quality.hourly is not None
        assert item.air_quality.hourly.pm2_5 is not None


# --- Batch Marine Forecast Tests ---


@pytest.mark.asyncio
async def test_batch_get_marine_forecasts_basic():
    """Test batch marine forecasts for multiple ocean locations."""
    # Hawaii, mid-Atlantic
    result = await batch_get_marine_forecasts(
        latitudes="21.31,0.0",
        longitudes="-157.86,0.0",
    )

    assert isinstance(result, BatchMarineForecastResponse)
    assert result.total_locations == 2
    assert len(result.results) == 2
    for i, item in enumerate(result.results):
        assert item.location_index == i
        assert item.forecast.hourly is not None
        assert item.forecast.hourly.wave_height is not None


@pytest.mark.asyncio
async def test_batch_get_marine_forecasts_single():
    """Test batch marine forecast with single location."""
    result = await batch_get_marine_forecasts(
        latitudes="21.31",
        longitudes="-157.86",
    )

    assert isinstance(result, BatchMarineForecastResponse)
    assert result.total_locations == 1
    assert result.results[0].location_index == 0


@pytest.mark.asyncio
async def test_batch_get_marine_forecasts_with_daily():
    """Test batch marine forecast with daily parameters."""
    result = await batch_get_marine_forecasts(
        latitudes="21.31,0.0",
        longitudes="-157.86,0.0",
        daily="wave_height_max,wave_direction_dominant",
        forecast_days=3,
    )

    assert isinstance(result, BatchMarineForecastResponse)
    assert result.total_locations == 2
    for item in result.results:
        assert item.forecast.daily is not None
        assert item.forecast.daily.wave_height_max is not None


# --- Batch Historical Weather Tests ---


@pytest.mark.asyncio
async def test_batch_get_historical_weather_basic():
    """Test batch historical weather for multiple locations."""
    # London, Paris
    result = await batch_get_historical_weather(
        latitudes="51.51,48.86",
        longitudes="-0.13,2.35",
        start_date="2024-01-01",
        end_date="2024-01-07",
        daily="temperature_2m_max,temperature_2m_min",
    )

    assert isinstance(result, BatchHistoricalWeatherResponse)
    assert result.total_locations == 2
    assert len(result.results) == 2
    for i, item in enumerate(result.results):
        assert item.location_index == i
        assert item.weather.daily is not None
        assert item.weather.daily.temperature_2m_max is not None


@pytest.mark.asyncio
async def test_batch_get_historical_weather_single():
    """Test batch historical weather with single location."""
    result = await batch_get_historical_weather(
        latitudes="51.51",
        longitudes="-0.13",
        start_date="2024-06-01",
        end_date="2024-06-02",
        hourly="temperature_2m,precipitation",
    )

    assert isinstance(result, BatchHistoricalWeatherResponse)
    assert result.total_locations == 1
    assert result.results[0].location_index == 0
    assert result.results[0].weather.hourly is not None


# --- Batch Weather Code Tests ---


@pytest.mark.asyncio
async def test_batch_interpret_weather_codes_basic():
    """Test batch interpretation of multiple weather codes."""
    result = await batch_interpret_weather_codes(weather_codes="3,51,61,95")

    assert isinstance(result, BatchWeatherCodeResponse)
    assert result.total_codes == 4
    assert len(result.results) == 4
    # Verify known codes
    assert result.results[0].code == 3
    assert result.results[0].description == "Overcast"
    assert result.results[0].severity == "cloudy"
    assert result.results[1].code == 51
    assert result.results[1].description == "Light drizzle"
    assert result.results[1].severity == "drizzle"
    assert result.results[2].code == 61
    assert result.results[2].severity == "rain"
    assert result.results[3].code == 95
    assert result.results[3].severity == "thunderstorm"


@pytest.mark.asyncio
async def test_batch_interpret_weather_codes_single():
    """Test batch interpretation with a single code."""
    result = await batch_interpret_weather_codes(weather_codes="0")

    assert isinstance(result, BatchWeatherCodeResponse)
    assert result.total_codes == 1
    assert result.results[0].code == 0
    assert result.results[0].description == "Clear sky"
    assert result.results[0].severity == "clear"


@pytest.mark.asyncio
async def test_batch_interpret_weather_codes_whitespace():
    """Test that whitespace around codes is trimmed."""
    result = await batch_interpret_weather_codes(weather_codes="0 , 3 , 45")

    assert isinstance(result, BatchWeatherCodeResponse)
    assert result.total_codes == 3
    assert result.results[0].code == 0
    assert result.results[1].code == 3
    assert result.results[2].code == 45


@pytest.mark.asyncio
async def test_batch_interpret_weather_codes_empty():
    """Test batch interpretation with empty input."""
    result = await batch_interpret_weather_codes(weather_codes="")

    assert isinstance(result, BatchWeatherCodeResponse)
    assert result.total_codes == 0
    assert len(result.results) == 0


@pytest.mark.asyncio
async def test_batch_interpret_weather_codes_unknown():
    """Test batch interpretation with unknown codes."""
    result = await batch_interpret_weather_codes(weather_codes="0,50,99")

    assert isinstance(result, BatchWeatherCodeResponse)
    assert result.total_codes == 3
    assert result.results[0].severity == "clear"
    # Code 50 is not in WMO codes
    assert result.results[1].code == 50
    assert result.results[1].severity == "unknown"
    assert result.results[2].severity == "thunderstorm"
