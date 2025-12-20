"""
Application configuration management using Pydantic.

Supports multiple environments (local, ci, staging, prod) with
environment-specific base URLs, timeouts, and credentials.

Environment variables can be loaded from:
1. System environment variables
2. .env file (loaded automatically)
3. CLI arguments (via pytest)
"""

from enum import Enum
from typing import Optional

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Supported environments."""

    LOCAL = "local"
    CI = "ci"
    STAGING = "staging"
    PROD = "prod"


class APISettings(BaseSettings):
    """API Configuration."""

    base_url: str = Field(
        default="https://jsonplaceholder.typicode.com",
        description="Base URL for API endpoints",
    )
    timeout: int = Field(
        default=10,
        description="Request timeout in seconds",
    )
    retries: int = Field(
        default=3,
        description="Number of retry attempts for failed requests",
    )
    retry_backoff: float = Field(
        default=0.5,
        description="Backoff factor for retries",
    )

    model_config = SettingsConfigDict(
        env_prefix="API_",
        case_sensitive=False,
    )


class UISettings(BaseSettings):
    """UI/Browser Configuration."""

    base_url: str = Field(
        default="https://www.saucedemo.com",
        description="Base URL for UI tests",
    )
    browser: str = Field(
        default="chromium",
        description="Browser to use (chromium, firefox, webkit)",
    )
    headless: bool = Field(
        default=True,
        description="Run browser in headless mode",
    )
    slow_motion: int = Field(
        default=0,
        description="Slow down browser actions (ms)",
    )
    timeout: int = Field(
        default=30_000,
        description="Playwright timeout in milliseconds",
    )
    viewport_width: int = Field(
        default=1280,
        description="Browser viewport width",
    )
    viewport_height: int = Field(
        default=720,
        description="Browser viewport height",
    )

    model_config = SettingsConfigDict(
        env_prefix="UI_",
        case_sensitive=False,
    )


class LoggingSettings(BaseSettings):
    """Logging Configuration."""

    level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format",
    )
    file: Optional[str] = Field(
        default=None,
        description="Log file path (optional)",
    )

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        case_sensitive=False,
    )


class Settings(BaseSettings):
    """
    Main application settings.

    Loads configuration from environment variables and .env file.
    Environment-specific overrides are applied based on ENV setting.
    """

    # Environment
    environment: Environment = Field(
        default=Environment.LOCAL,
        description="Current environment (local, ci, staging, prod)",
    )

    # Nested settings
    api: APISettings = Field(default_factory=APISettings)
    ui: UISettings = Field(default_factory=UISettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    # Feature flags
    record_video: bool = Field(
        default=False,
        description="Record video of UI test runs",
    )
    record_trace: bool = Field(
        default=False,
        description="Record Playwright trace for debugging",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",  # Allow extra fields from env vars
    )

    @validator("environment", pre=True)
    def parse_environment(cls, v: str) -> Environment:
        """Parse environment string to Environment enum."""
        if isinstance(v, Environment):
            return v
        return Environment(v.lower())

    @validator("api", pre=True, always=True)
    def load_api_settings(cls, v: APISettings, values: dict) -> APISettings:
        """Load API settings with environment-specific overrides."""
        if isinstance(v, APISettings):
            return v
        return APISettings()

    @validator("ui", pre=True, always=True)
    def load_ui_settings(cls, v: UISettings, values: dict) -> UISettings:
        """Load UI settings with environment-specific overrides."""
        if isinstance(v, UISettings):
            return v
        return UISettings()

    @validator("logging", pre=True, always=True)
    def load_logging_settings(cls, v: LoggingSettings, values: dict) -> LoggingSettings:
        """Load logging settings."""
        if isinstance(v, LoggingSettings):
            return v
        return LoggingSettings()

    def __str__(self) -> str:
        """Return string representation of settings."""
        return (
            f"Settings(environment={self.environment}, "
            f"api_url={self.api.base_url}, "
            f"ui_url={self.ui.base_url})"
        )


# Global settings instance (lazy-loaded)
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create global settings instance.

    Returns:
        Settings: Global settings object

    Example:
        >>> settings = get_settings()
        >>> print(settings.api.base_url)
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def load_settings(environment: Optional[str] = None) -> Settings:
    """
    Load settings, optionally overriding environment.

    Args:
        environment: Environment to load (local, ci, staging, prod)

    Returns:
        Settings: Loaded settings object

    Example:
        >>> settings = load_settings("staging")
        >>> print(settings.api.base_url)
    """
    global _settings
    if environment:
        _settings = Settings(environment=environment)
    else:
        _settings = Settings()
    return _settings