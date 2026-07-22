class AgentError(Exception):
    """Base exception for all agent-related errors."""
    pass


class ConnectorError(AgentError):
    """Raised when a connector fails."""
    pass


class ConfigurationError(AgentError):
    """Raised for invalid configuration."""
    pass


class ValidationError(AgentError):
    """Raised when validation fails."""
    pass