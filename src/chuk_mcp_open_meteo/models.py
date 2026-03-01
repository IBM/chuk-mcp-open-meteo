"""Pydantic models for Open-Meteo API responses.

All API responses are properly typed using Pydantic models for type safety,
validation, and better IDE support.
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Weather Forecast Models
class CurrentWeather(BaseModel):
    """Current weather conditions snapshot.

    Use weathercode with interpret_weather_code tool for human-readable description.
    """

    temperature: float = Field(
        ..., description="Current temperature in requested unit (celsius or fahrenheit)"
    )
    windspeed: float = Field(
        ..., description="Current wind speed in requested unit (km/h, m/s, mph, or knots)"
    )
    winddirection: float = Field(
        ...,
        description="Wind direction in degrees (0-360, meteorological: 0=from North, 90=from East, "
        "180=from South, 270=from West)",
    )
    weathercode: int = Field(
        ...,
        description="WMO weather code (0-99). Use interpret_weather_code tool to get description. "
        "Common: 0=clear, 1-3=cloudy, 45/48=fog, 51-67=rain/drizzle, 71-77=snow, 95-99=thunderstorm",
    )
    time: str = Field(..., description="ISO 8601 timestamp of current conditions")


class HourlyWeather(BaseModel):
    """Hourly weather forecast data with 50+ available variables.

    All lists are parallel arrays - use the same index across all fields for a specific hour.
    Example: temperature_2m[0] is the temperature for time[0].
    """

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    time: list[str] = Field(..., description="ISO 8601 timestamps for each hour")
    temperature_2m: Optional[list[float]] = Field(
        None, description="Temperature at 2 meters height in requested unit"
    )
    relative_humidity_2m: Optional[list[float]] = Field(
        None, description="Relative humidity at 2 meters (0-100%)"
    )
    precipitation: Optional[list[float]] = Field(
        None,
        description="Total precipitation (rain + snow + showers) in requested unit (mm or inch). "
        "0=no precipitation",
    )
    rain: Optional[list[float]] = Field(
        None, description="Rain amount only (excluding snow/showers)"
    )
    showers: Optional[list[float]] = Field(None, description="Shower precipitation amount")
    snowfall: Optional[list[float]] = Field(None, description="Snowfall amount in cm or inch")
    cloud_cover: Optional[list[float]] = Field(
        None, description="Total cloud cover percentage (0-100%). 0=clear, 100=overcast"
    )
    wind_speed_10m: Optional[list[float]] = Field(
        None, description="Wind speed at 10 meters height in requested unit"
    )
    wind_direction_10m: Optional[list[float]] = Field(
        None,
        description="Wind direction at 10m in degrees (0-360, from North=0, East=90, South=180, West=270)",
    )
    pressure_msl: Optional[list[float]] = Field(
        None, description="Atmospheric pressure at sea level in hPa"
    )


class DailyWeather(BaseModel):
    """Daily weather forecast summary data.

    Provides daily aggregates - high/low temps, totals, and key times.
    All lists are parallel arrays indexed by day.
    """

    model_config = ConfigDict(extra="allow")  # Allow additional fields from API

    time: list[str] = Field(..., description="ISO 8601 dates (YYYY-MM-DD format)")
    temperature_2m_max: Optional[list[float]] = Field(
        None, description="Maximum (high) temperature for the day in requested unit"
    )
    temperature_2m_min: Optional[list[float]] = Field(
        None, description="Minimum (low) temperature for the day in requested unit"
    )
    precipitation_sum: Optional[list[float]] = Field(
        None,
        description="Total precipitation for the day (rain + snow) in requested unit (mm or inch)",
    )
    precipitation_hours: Optional[list[float]] = Field(
        None, description="Number of hours with precipitation during the day (0-24)"
    )
    rain_sum: Optional[list[float]] = Field(
        None, description="Total rain for the day (excluding snow)"
    )
    sunrise: Optional[list[str]] = Field(None, description="Sunrise time in ISO 8601 format")
    sunset: Optional[list[str]] = Field(None, description="Sunset time in ISO 8601 format")
    wind_speed_10m_max: Optional[list[float]] = Field(
        None, description="Maximum wind speed during the day in requested unit"
    )


class WeatherForecast(BaseModel):
    """Complete weather forecast response."""

    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    elevation: Optional[float] = Field(None, description="Elevation in meters")
    timezone: Optional[str] = Field(None, description="Timezone name")
    timezone_abbreviation: Optional[str] = Field(None, description="Timezone abbreviation")
    current_weather: Optional[CurrentWeather] = Field(None, description="Current weather")
    hourly: Optional[HourlyWeather] = Field(None, description="Hourly forecast")
    daily: Optional[DailyWeather] = Field(None, description="Daily forecast")


# Geocoding Models
class GeocodingResult(BaseModel):
    """Single location result from geocoding."""

    id: Optional[int] = Field(None, description="Location ID")
    name: str = Field(..., description="Location name")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    elevation: Optional[float] = Field(None, description="Elevation in meters")
    feature_code: Optional[str] = Field(None, description="GeoNames feature code")
    country_code: Optional[str] = Field(None, description="ISO 3166-1 alpha-2 country code")
    country: Optional[str] = Field(None, description="Country name")
    country_id: Optional[int] = Field(None, description="Country ID")
    timezone: Optional[str] = Field(None, description="Timezone name")
    population: Optional[int] = Field(None, description="Population")
    postcodes: Optional[list[str]] = Field(None, description="Postcodes")
    admin1: Optional[str] = Field(None, description="Administrative division level 1")
    admin2: Optional[str] = Field(None, description="Administrative division level 2")
    admin3: Optional[str] = Field(None, description="Administrative division level 3")
    admin4: Optional[str] = Field(None, description="Administrative division level 4")


class GeocodingResponse(BaseModel):
    """Geocoding API response."""

    results: Optional[list[GeocodingResult]] = Field(None, description="List of matching locations")
    generationtime_ms: Optional[float] = Field(None, description="Generation time in ms")


# Historical Weather (uses same models as forecast)
class HistoricalWeather(BaseModel):
    """Historical weather response."""

    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    elevation: Optional[float] = Field(None, description="Elevation in meters")
    timezone: Optional[str] = Field(None, description="Timezone name")
    timezone_abbreviation: Optional[str] = Field(None, description="Timezone abbreviation")
    hourly: Optional[HourlyWeather] = Field(None, description="Hourly historical data")
    daily: Optional[DailyWeather] = Field(None, description="Daily historical data")


# Air Quality Models
class HourlyAirQuality(BaseModel):
    """Hourly air quality data."""

    model_config = ConfigDict(extra="allow")  # Allow additional fields (pollen, etc.)

    time: list[str] = Field(..., description="ISO 8601 timestamps")
    pm10: Optional[list[Optional[float]]] = Field(None, description="PM10 in µg/m³")
    pm2_5: Optional[list[Optional[float]]] = Field(None, description="PM2.5 in µg/m³")
    carbon_monoxide: Optional[list[Optional[float]]] = Field(None, description="CO in µg/m³")
    nitrogen_dioxide: Optional[list[Optional[float]]] = Field(None, description="NO2 in µg/m³")
    sulphur_dioxide: Optional[list[Optional[float]]] = Field(None, description="SO2 in µg/m³")
    ozone: Optional[list[Optional[float]]] = Field(None, description="O3 in µg/m³")
    dust: Optional[list[Optional[float]]] = Field(None, description="Dust in µg/m³")
    uv_index: Optional[list[Optional[float]]] = Field(None, description="UV index")
    us_aqi: Optional[list[Optional[int]]] = Field(None, description="US AQI")
    european_aqi: Optional[list[Optional[int]]] = Field(None, description="European AQI")


class AirQualityResponse(BaseModel):
    """Air quality API response."""

    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    elevation: Optional[float] = Field(None, description="Elevation in meters")
    timezone: Optional[str] = Field(None, description="Timezone name")
    hourly: Optional[HourlyAirQuality] = Field(None, description="Hourly air quality data")


# Marine Forecast Models
class HourlyMarine(BaseModel):
    """Hourly marine forecast data with wave, swell, and current information.

    Wave heights are in meters. For context:
    - 0-0.5m: Calm (safe swimming)
    - 0.5-1.5m: Small (beginner surfing)
    - 1.5-2.5m: Moderate (intermediate surfing)
    - 2.5-4m: Large (advanced surfing)
    - 4m+: Very large (dangerous)

    Wave period in seconds indicates quality:
    - <8s: Short/choppy (wind waves)
    - 8-12s: Medium (good surf)
    - 12s+: Long (excellent surf/swell)
    """

    model_config = ConfigDict(extra="allow")

    time: list[str] = Field(..., description="ISO 8601 timestamps for each hour")

    # Total wave characteristics (combined wind + swell)
    wave_height: Optional[list[Optional[float]]] = Field(
        None,
        description="Total significant wave height in meters (combined wind waves + swell). "
        "This is the primary metric for wave size. 0-0.5m=calm, 0.5-1.5m=small, "
        "1.5-2.5m=moderate, 2.5-4m=large, 4m+=very large/dangerous",
    )
    wave_direction: Optional[list[Optional[float]]] = Field(
        None,
        description="Wave direction in degrees (0-360, meteorological convention: 0=from North, "
        "90=from East, 180=from South, 270=from West)",
    )
    wave_period: Optional[list[Optional[float]]] = Field(
        None,
        description="Wave period in seconds (time between wave crests). Higher is better for surfing: "
        "<8s=choppy, 8-12s=good, 12s+=excellent",
    )

    # Wind waves (locally generated by current wind)
    wind_wave_height: Optional[list[Optional[float]]] = Field(
        None,
        description="Wind wave height in meters (waves generated by local wind, typically choppy). "
        "These are less organized than swell",
    )
    wind_wave_direction: Optional[list[Optional[float]]] = Field(
        None, description="Wind wave direction in degrees (0-360, meteorological convention)"
    )
    wind_wave_period: Optional[list[Optional[float]]] = Field(
        None,
        description="Wind wave period in seconds (usually shorter/choppier than swell)",
    )

    # Swell waves (from distant storms, more organized)
    swell_wave_height: Optional[list[Optional[float]]] = Field(
        None,
        description="Swell wave height in meters (waves from distant storms, clean and organized). "
        "These create the best surfing conditions",
    )
    swell_wave_direction: Optional[list[Optional[float]]] = Field(
        None,
        description="Swell wave direction in degrees (0-360, direction swell is coming FROM)",
    )
    swell_wave_period: Optional[list[Optional[float]]] = Field(
        None,
        description="Swell wave period in seconds (typically longer than wind waves, 10-20s indicates "
        "quality swell from distant storms)",
    )

    # Ocean currents
    ocean_current_velocity: Optional[list[Optional[float]]] = Field(
        None,
        description="Ocean current speed in meters/second. Important for safety: >1 m/s is strong, "
        ">2 m/s is dangerous for swimming",
    )
    ocean_current_direction: Optional[list[Optional[float]]] = Field(
        None,
        description="Ocean current direction in degrees (0-360, direction current is flowing TOWARDS)",
    )

    # Tides and sea level
    sea_level_height_msl: Optional[list[Optional[float]]] = Field(
        None,
        description="Sea level height in meters relative to mean sea level, accounting for tides, inverted "
        "barometer effect, and sea surface height variations. Positive values indicate higher water, "
        "negative values indicate lower water. Use this for tide predictions and timing beach/surf activities. "
        "The tidal cycle is clearly visible in this data (high/low tides every ~6 hours). "
        "Note: Accuracy is limited in coastal areas - use with caution and not for navigation.",
    )


class DailyMarine(BaseModel):
    """Daily marine forecast data."""

    model_config = ConfigDict(extra="allow")

    time: list[str] = Field(..., description="ISO 8601 dates")
    wave_height_max: Optional[list[Optional[float]]] = Field(
        None, description="Maximum wave height"
    )
    wave_direction_dominant: Optional[list[Optional[float]]] = Field(
        None, description="Dominant wave direction"
    )
    wave_period_max: Optional[list[Optional[float]]] = Field(
        None, description="Maximum wave period"
    )


class MarineForecast(BaseModel):
    """Marine forecast API response."""

    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    elevation: Optional[float] = Field(None, description="Elevation in meters")
    timezone: Optional[str] = Field(None, description="Timezone name")
    hourly: Optional[HourlyMarine] = Field(None, description="Hourly marine forecast")
    daily: Optional[DailyMarine] = Field(None, description="Daily marine forecast")


# Weather Code Interpretation
class WeatherCodeInterpretation(BaseModel):
    """Interpretation of WMO weather code."""

    code: int = Field(..., description="WMO weather code number (0-99)")
    description: str = Field(..., description="Human-readable weather condition description")
    severity: str = Field(
        ...,
        description="Weather severity category: clear, cloudy, fog, drizzle, rain, freezing, snow, showers, thunderstorm, unknown",
    )


# Batch Response Models
class BatchWeatherCodeItem(BaseModel):
    """A single weather code interpretation within a batch response."""

    code: int = Field(..., description="WMO weather code number (0-99)")
    description: str = Field(..., description="Human-readable weather condition description")
    severity: str = Field(
        ...,
        description="Weather severity category: clear, cloudy, fog, drizzle, rain, freezing, snow, showers, thunderstorm, unknown",
    )


class BatchWeatherCodeResponse(BaseModel):
    """Response from batch weather code interpretation."""

    results: list[BatchWeatherCodeItem] = Field(
        ..., description="Interpretations for each weather code, in the same order as input"
    )
    total_codes: int = Field(..., description="Total number of codes submitted")


class BatchGeocodingItem(BaseModel):
    """Result for a single location in a batch geocoding request."""

    query: str = Field(..., description="The original location name that was searched")
    found: bool = Field(..., description="Whether any results were found for this query")
    results: Optional[list[GeocodingResult]] = Field(
        None, description="List of matching locations (None if not found)"
    )
    error: Optional[str] = Field(
        None, description="Error message if the geocoding request failed for this location"
    )


class BatchGeocodingResponse(BaseModel):
    """Response from batch geocoding multiple locations concurrently."""

    results: list[BatchGeocodingItem] = Field(
        ..., description="Results for each queried location, in the same order as the input"
    )
    total_queries: int = Field(..., description="Total number of location queries submitted")
    successful: int = Field(
        ..., description="Number of locations that returned at least one result"
    )
    failed: int = Field(
        ..., description="Number of locations that returned no results or had errors"
    )


class BatchWeatherForecastItem(BaseModel):
    """A single forecast within a batch response, tagged with a location index."""

    location_index: int = Field(
        ...,
        description="Zero-based index corresponding to the position in the input latitude/longitude arrays",
    )
    forecast: WeatherForecast = Field(
        ..., description="The weather forecast data for this location"
    )


class BatchWeatherForecastResponse(BaseModel):
    """Response from batch weather forecast for multiple locations."""

    results: list[BatchWeatherForecastItem] = Field(
        ..., description="Weather forecasts for each location, indexed by position in input arrays"
    )
    total_locations: int = Field(..., description="Total number of locations queried")


class BatchAirQualityItem(BaseModel):
    """A single air quality result within a batch response."""

    location_index: int = Field(
        ...,
        description="Zero-based index corresponding to the position in the input latitude/longitude arrays",
    )
    air_quality: AirQualityResponse = Field(
        ..., description="The air quality data for this location"
    )


class BatchAirQualityResponse(BaseModel):
    """Response from batch air quality query for multiple locations."""

    results: list[BatchAirQualityItem] = Field(
        ..., description="Air quality data for each location, indexed by position in input arrays"
    )
    total_locations: int = Field(..., description="Total number of locations queried")


class BatchMarineForecastItem(BaseModel):
    """A single marine forecast within a batch response."""

    location_index: int = Field(
        ...,
        description="Zero-based index corresponding to the position in the input latitude/longitude arrays",
    )
    forecast: MarineForecast = Field(..., description="The marine forecast data for this location")


class BatchMarineForecastResponse(BaseModel):
    """Response from batch marine forecast for multiple locations."""

    results: list[BatchMarineForecastItem] = Field(
        ..., description="Marine forecasts for each location, indexed by position in input arrays"
    )
    total_locations: int = Field(..., description="Total number of locations queried")


class BatchHistoricalWeatherItem(BaseModel):
    """A single historical weather result within a batch response."""

    location_index: int = Field(
        ...,
        description="Zero-based index corresponding to the position in the input latitude/longitude arrays",
    )
    weather: HistoricalWeather = Field(
        ..., description="The historical weather data for this location"
    )


class BatchHistoricalWeatherResponse(BaseModel):
    """Response from batch historical weather query for multiple locations."""

    results: list[BatchHistoricalWeatherItem] = Field(
        ...,
        description="Historical weather data for each location, indexed by position in input arrays",
    )
    total_locations: int = Field(..., description="Total number of locations queried")
