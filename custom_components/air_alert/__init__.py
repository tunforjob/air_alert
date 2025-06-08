"""
Air Alert integration for Home Assistant.
"""

import logging

DOMAIN = "air_alert"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the Air Alert component."""
    return True


async def async_setup_entry(hass, entry):
    """Set up Air Alert from a config entry."""
    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return True
