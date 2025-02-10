# core/logging_config.py

import logging


def setup_logging(level=logging.INFO):
    """Configures the logging level for the application."""
    logging.basicConfig(
        format="%(levelname)s:%(name)s:%(message)s",
        level=level,
    )

def set_logging_level(level_name, verbose=False):
    """Updates the logging level dynamically.

    :param level_name: String (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    :param verbose: Boolean (Enables full detailed logs)
    """
    level = logging.DEBUG if verbose else getattr(logging, level_name.upper(), None)
    if level is None:
        raise ValueError(f"Invalid logging level: {level_name}")
    logging.getLogger().setLevel(level)
