"""
Sensor platform for Air Alert integration.
"""

import logging
import voluptuous as vol
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL
from homeassistant.util import Throttle

from alerts_in_ua import Client as AlertsClient

DOMAIN = "air_alert"
_LOGGER = logging.getLogger(__name__)

# Scan interval for the sensor
SCAN_INTERVAL = timedelta(seconds=60)

# Configuration constants
CONF_API_TOKEN = "api_token"
CONF_REGION_TYPE = "region_type"
CONF_REGION_NAME = "region_name"
CONF_LOCATION_UID = "location_uid"
DEFAULT_NAME = "Air Alert"
DEFAULT_REGION_TYPE = "location_oblast"
DEFAULT_REGION_NAME = "Kyiv"
DEFAULT_LOCATION_UID = None
DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

# Schema for the configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_TOKEN): cv.string,
        vol.Optional(CONF_REGION_TYPE, default=DEFAULT_REGION_TYPE): cv.string,
        vol.Optional(CONF_REGION_NAME, default=DEFAULT_REGION_NAME): cv.string,
        vol.Optional(CONF_LOCATION_UID): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Air Alert sensor."""
    name = config.get(CONF_NAME)
    api_token = config.get(CONF_API_TOKEN)
    region_type = config.get(CONF_REGION_TYPE)
    region_name = config.get(CONF_REGION_NAME)
    location_uid = config.get(CONF_LOCATION_UID)
    scan_interval = config.get(CONF_SCAN_INTERVAL)

    # Create the alerts client
    try:
        alerts_client = AlertsClient(token=api_token)
    except Exception as ex:
        _LOGGER.error("Error initializing alerts.in.ua client: %s", ex)
        return False

    # Create and add sensor entity
    sensor = AirAlertSensor(
        hass, name, alerts_client, region_type, region_name, location_uid, scan_interval
    )
    add_entities([sensor], True)


class AirAlertSensor(Entity):
    """Representation of an Air Alert Sensor."""

    def __init__(
        self,
        hass,
        name,
        alerts_client,
        region_type,
        region_name,
        location_uid,
        scan_interval,
    ):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._alerts_client = alerts_client
        self._region_type = region_type
        self._region_name = region_name
        self._location_uid = location_uid
        self._scan_interval = scan_interval
        self._state = None
        self._attributes = {}
        if location_uid:
            self._attributes["location_uid"] = location_uid
        else:
            self._attributes["region_type"] = region_type
            self._attributes["region_name"] = region_name
        self._last_updated = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID for this entity."""
        # Create a unique ID based on the location_uid if available, otherwise use region name and type
        if self._location_uid:
            return f"air_alert_uid_{self._location_uid}"
        else:
            return f"air_alert_{self._region_type}_{self._region_name}".lower().replace(
                " ", "_"
            )

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self._state == "Alert":
            return "mdi:alert"
        return "mdi:shield"

    def update(self):
        """Fetch new state data for the sensor."""
        self._update_alert_status()

    @Throttle(SCAN_INTERVAL)
    def _update_alert_status(self):
        """Update alert status from the API."""

        try:
            # Get active alerts
            active_alerts = self._alerts_client.get_active_alerts()

            # Check for alerts based on configuration
            if self._location_uid:
                # Filter by location_uid if provided
                region_alerts = active_alerts.get_alerts_by_location_uid(
                    self._location_uid
                )
            else:
                # Otherwise filter by region type and name
                region_alerts = active_alerts.filter(
                    self._region_type, self._region_name
                )

            # Update state and attributes
            if region_alerts:
                self._state = "Alert"
                self._attributes.update(
                    {
                        "alert_count": len(region_alerts),
                        "alert_type": region_alerts[0].alert_type
                        if region_alerts
                        else None,
                        "started_at": region_alerts[0].started_at.isoformat()
                        if region_alerts
                        else None,
                    }
                )
            else:
                self._state = "Clear"
                self._attributes.update({"alert_count": 0})

            location_info = (
                self._location_uid if self._location_uid else self._region_name
            )
            _LOGGER.info(f"Updated air alert status for {location_info}: {self._state}")

        except Exception as ex:
            _LOGGER.error("Error updating alert status: %s", ex)
            self._state = "Error"
            self._attributes = {"error": str(ex)}
