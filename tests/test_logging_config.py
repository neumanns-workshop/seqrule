import logging

import pytest

from seqrule import set_logging_level, setup_logging


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration after each test."""
    yield
    logging.getLogger().setLevel(logging.INFO)
    # Reset any handlers that might have been added
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)


def test_setup_logging():
    """Test basic logging setup."""
    # Remove any existing handlers
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    setup_logging()
    assert logging.getLogger().level == logging.INFO
    assert len(logging.getLogger().handlers) > 0

    # Remove handlers again for next test
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    setup_logging(level=logging.DEBUG)
    assert logging.getLogger().level == logging.DEBUG
    assert len(logging.getLogger().handlers) > 0


def test_set_logging_level():
    """Test dynamic logging level updates."""
    # Test valid levels
    set_logging_level("INFO")
    assert logging.getLogger().level == logging.INFO

    set_logging_level("DEBUG")
    assert logging.getLogger().level == logging.DEBUG

    set_logging_level("WARNING")
    assert logging.getLogger().level == logging.WARNING

    set_logging_level("ERROR")
    assert logging.getLogger().level == logging.ERROR

    set_logging_level("CRITICAL")
    assert logging.getLogger().level == logging.CRITICAL


def test_set_logging_level_verbose():
    """Test verbose mode setting."""
    set_logging_level("INFO", verbose=True)
    assert logging.getLogger().level == logging.DEBUG

    set_logging_level("ERROR", verbose=True)
    assert logging.getLogger().level == logging.DEBUG  # Verbose always sets DEBUG


def test_invalid_logging_level():
    """Test handling of invalid logging levels."""
    with pytest.raises(ValueError) as exc_info:
        set_logging_level("INVALID_LEVEL")
    assert "Invalid logging level" in str(exc_info.value)
