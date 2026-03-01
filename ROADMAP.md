# Roadmap

This document outlines the development roadmap for chuk-mcp-open-meteo.

## Completed

### v1.0 — Core Tools
- `get_weather_forecast` — current conditions, hourly, and daily forecasts with 50+ variables
- `geocode_location` — location name to coordinate lookup with worldwide coverage
- `get_historical_weather` — archive data from 1940 onwards
- `get_air_quality` — pollutants, AQI indices, pollen, UV
- `get_marine_forecast` — waves, swell, currents, tides via `sea_level_height_msl`
- `interpret_weather_code` — WMO code translation with severity categories
- Pydantic v2 models for all responses with LLM-friendly field descriptions
- STDIO and HTTP transport modes
- Docker, Fly.io, and Claude Desktop deployment
- Public hosted server at `weather.chukai.io`

### v1.1 — Batch Operations
- `batch_geocode_locations` — geocode multiple locations concurrently in a single tool call
  - Comma-separated input, concurrent execution with connection pooling
  - Semaphore-based concurrency cap (10 parallel requests)
  - Partial failure handling per location
- `batch_get_weather_forecasts` — fetch forecasts for multiple locations in one API call
  - Uses Open-Meteo's native multi-location support (up to 1000 locations)
  - Single HTTP request for all locations
- `batch_get_air_quality` — air quality for multiple locations in one API call
  - Same native comma-separated lat/lon pattern
  - Defaults to common pollutant metrics when no hourly variables specified
- `batch_get_marine_forecasts` — marine conditions for multiple coastal points
  - Waves, swell, currents, and tides across multiple ocean locations
  - Useful for "surf conditions along the coast" queries
- `batch_get_historical_weather` — historical data for multiple locations
  - All locations share the same date range in a single API call
  - Supports both hourly and daily variables
- `batch_interpret_weather_codes` — interpret multiple WMO codes in a single call
  - Comma-separated input: `"3,51,61,95"` → all interpretations at once
  - Eliminates N sequential `interpret_weather_code` calls after batch forecasts
  - Handles unknown codes and invalid input gracefully
- Batch Pydantic models for all 6 batch tools (12 new models total)

### v1.2 — Architectural Refactor
- Decomposed monolithic `server.py` (1155 lines) into focused modules
  - `tools/` package with 6 domain modules (forecast, geocoding, historical, air_quality, marine, weather_codes)
  - `_constants.py` — API URLs, default hourly variables, weather codes (no magic strings)
  - `_batch.py` — generic `batch_fetch()` helper eliminates duplicated code across 4 batch tools
  - `server.py` reduced to thin entry point (~65 lines)
- Normalized all batch response models to use `results` field consistently
- Backward-compatible re-exports from `server.py` for existing imports

---

## Planned

### Composite Tools — High-Level Multi-Step Operations
Single tools that combine geocoding + data fetch for common workflows.

- [ ] `get_weather_for_locations` — names in, weather out (geocode + forecast in one call)
  - Input: `"London,Paris,Berlin"` → Output: named weather results
  - Uses `batch_geocode_locations` + `batch_get_weather_forecasts` internally
  - Handles disambiguation automatically (first result per location)
  - Reduces LLM round-trips from 2 to 1 for the most common multi-location query
- [ ] `compare_weather` — side-by-side weather comparison for multiple locations
  - Returns a structured comparison (temp ranges, precipitation, wind) rather than raw forecasts
  - Designed for "compare weather in London vs Paris vs Berlin" queries

### Alerts & Conditions — Derived Intelligence
Tools that interpret raw data into actionable recommendations.

- [ ] `get_weather_alerts` — severe weather warnings for a location
  - Analyze forecast data for dangerous conditions (high wind, heavy rain, extreme temps, thunderstorms)
  - Return structured alerts with severity levels and time windows
  - No new API needed — derived from existing forecast data
- [ ] `get_activity_recommendation` — weather suitability for activities
  - Input: location + activity type (hiking, surfing, skiing, outdoor dining, etc.)
  - Output: suitability score + reasoning based on forecast, marine, and air quality data
  - Combines multiple data sources into a single recommendation

### Caching Layer
Reduce API calls and improve latency for repeated queries.

- [ ] In-memory TTL cache for geocoding results (locations rarely change)
  - Cache key: normalized location name + count + language
  - TTL: 24 hours (geocoding data is stable)
- [ ] Short-lived cache for weather data
  - Cache key: coordinates (rounded to 2 decimal places) + parameters
  - TTL: 15 minutes (weather data updates hourly)
- [ ] Cache statistics exposed via a `get_cache_stats` tool for observability

### Enhanced Error Handling
- [ ] Structured error responses with error codes and retry guidance
- [ ] Automatic retry with exponential backoff for transient API failures
- [ ] Rate limit detection and backoff for batch operations
- [ ] Input validation (lat/lon ranges, date formats) before making API calls

---

## Future Considerations

### Additional Open-Meteo APIs
- [ ] **Flood API** — river discharge forecasts and flood warnings
- [ ] **Climate Change API** — projected temperature/precipitation changes by decade
- [ ] **Elevation API** — get elevation for any coordinate
- [ ] **Ensemble Models** — probabilistic forecasts with confidence intervals

### MCP Resources
- [ ] Expose weather data as MCP resources (not just tools)
  - `weather://{city}/current` — subscribable current conditions
  - `weather://{city}/forecast` — subscribable forecast updates
  - Enables real-time weather dashboards via MCP resource subscriptions

### MCP Prompts
- [ ] Pre-built prompt templates for common workflows
  - "Trip weather planner" — multi-city weather comparison with packing suggestions
  - "Marine activity advisor" — surf/sail/fish conditions with tide analysis
  - "Air quality monitor" — pollution tracking with health recommendations

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Feature requests and pull requests welcome — especially for items marked with `[ ]` above.
