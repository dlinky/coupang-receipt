"""Custom exceptions for settlement automation application."""


class SettlementAutomationError(Exception):
    """Base exception for settlement automation."""
    pass


class FileError(SettlementAutomationError):
    """File-related errors."""
    pass


class MappingError(SettlementAutomationError):
    """Mapping-related errors."""
    pass


class DataError(SettlementAutomationError):
    """Data-related errors."""
    pass


class SystemError(SettlementAutomationError):
    """System-related errors."""
    pass

