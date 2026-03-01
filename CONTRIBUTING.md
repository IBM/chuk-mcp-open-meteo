# Contributing to Chuk MCP Open-Meteo

Thank you for your interest in contributing to the best weather MCP server ever! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- UV (recommended) or pip

### Getting Started

1. **Fork and Clone**

```bash
git clone https://github.com/YOUR_USERNAME/chuk-mcp-open-meteo.git
cd chuk-mcp-open-meteo
```

2. **Install Dependencies**

Using UV (recommended):
```bash
uv sync --dev
```

Using pip:
```bash
pip install -e ".[dev]"
```

3. **Verify Installation**

```bash
make test
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

Follow these guidelines:

- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed
- Follow the existing code style

### 3. Test Your Changes

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run linting
make lint

# Run type checking
make typecheck

# Run all checks
make check
```

### 4. Format Code

```bash
make format
```

This will auto-format your code using Ruff.

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add awesome new feature"
```

Use conventional commit messages:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

We use Ruff for linting and formatting:

- Line length: 100 characters
- Type hints required for public APIs
- Docstrings for all public functions and classes
- Follow PEP 8 conventions

## Adding New Tools

When adding a new weather tool:

1. **Add the tool function** in `src/chuk_mcp_open_meteo/server.py`:

```python
@tool
async def your_new_tool(
    latitude: float,
    longitude: float,
    # ... other parameters
) -> dict[str, Any]:
    """Clear description of what the tool does.

    Args:
        latitude: Description
        longitude: Description

    Returns:
        Description of return value
    """
    # Implementation
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
```

2. **Add documentation** in README.md
3. **Add usage examples** in examples/usage_examples.md
4. **Add tests** (when test infrastructure is added)

## Documentation

Update these files when making changes:

- `README.md` - Main documentation
- `CONTRIBUTING.md` - This file
- `examples/usage_examples.md` - Usage examples
- Docstrings in code

## Testing

### Writing Tests

Tests should be added to the `tests/` directory (to be created):

```python
# tests/test_server.py
import pytest
from chuk_mcp_open_meteo.server import get_weather_forecast

@pytest.mark.asyncio
async def test_get_weather_forecast():
    result = await get_weather_forecast(
        latitude=51.5072,
        longitude=-0.1276
    )
    assert "latitude" in result
    assert "current_weather" in result
```

### Running Tests

```bash
# All tests
make test

# With coverage
make test-cov

# Specific test file
pytest tests/test_server.py

# Specific test
pytest tests/test_server.py::test_get_weather_forecast
```

## Release Process

Releases are automated via GitHub Actions:

1. **Bump Version**

```bash
make bump-patch  # 1.0.0 -> 1.0.1
make bump-minor  # 1.0.0 -> 1.1.0
make bump-major  # 1.0.0 -> 2.0.0
```

2. **Commit Version Change**

```bash
git add pyproject.toml
git commit -m "chore: bump version to X.Y.Z"
git push
```

3. **Create Release**

```bash
make publish
```

This will:
- Create and push a git tag
- Trigger GitHub Actions
- Create a GitHub release
- Publish to PyPI

## Project Structure

```
chuk-mcp-open-meteo/
├── src/
│   └── chuk_mcp_open_meteo/
│       ├── __init__.py
│       ├── server.py          # Thin entry point — imports tools, runs server
│       ├── models.py          # All Pydantic v2 response models
│       ├── _constants.py      # API URLs, default parameters, weather codes
│       ├── _batch.py          # Generic batch fetch helper
│       └── tools/             # Domain-focused tool modules
│           ├── forecast.py    # get_weather_forecast + batch_get_weather_forecasts
│           ├── geocoding.py   # geocode_location + batch_geocode_locations
│           ├── historical.py  # get_historical_weather + batch_get_historical_weather
│           ├── air_quality.py # get_air_quality + batch_get_air_quality
│           ├── marine.py      # get_marine_forecast + batch_get_marine_forecasts
│           └── weather_codes.py # interpret_weather_code + batch_interpret_weather_codes
├── tests/                      # Test files
├── examples/                   # Usage examples
├── .github/
│   └── workflows/             # CI/CD workflows
├── pyproject.toml             # Project configuration
├── Makefile                   # Development commands
├── Dockerfile                 # Docker configuration
├── fly.toml                   # Fly.io deployment config
└── README.md                  # Main documentation
```

## API Guidelines

### Open-Meteo API Usage

- Use async/await for all API calls
- Always use `httpx.AsyncClient()` as context manager
- Set reasonable timeouts (30s default)
- Handle HTTP errors gracefully
- Follow Open-Meteo's [fair use policy](https://open-meteo.com/en/terms)

### Tool Design Principles

1. **Simple by default**: Provide sensible defaults
2. **Comprehensive when needed**: Allow detailed customization
3. **Type-safe**: Use proper type hints
4. **Well-documented**: Clear docstrings with examples
5. **Error-friendly**: Helpful error messages

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions or share ideas
- **Pull Requests**: Contribute code or documentation

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes
- Project documentation

Thank you for contributing to making this the best weather MCP server ever!
