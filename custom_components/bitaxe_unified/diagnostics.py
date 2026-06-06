from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.components.diagnostics import async_redact_data

from .const import CONF_HOST, DOMAIN

TO_REDACT = {CONF_HOST, "host", "hostname", "ssid", "wifiSSID", "stratumURL", "stratumUser", "stratumPassword", "fallbackStratumURL", "fallbackStratumUser", "fallbackStratumPassword"}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    data = {
        "entry": dict(entry.data),
        "device_name": coordinator.device_name,
        "last_update_success": coordinator.last_update_success,
        "endpoint_errors": coordinator.data.get("endpoint_errors", {}) if coordinator.data else {},
        "api_payloads": {k: v for k, v in (coordinator.data or {}).items() if k not in {"flat"}},
        "flat_keys": sorted((coordinator.data or {}).get("flat", {}).keys()),
    }
    return async_redact_data(data, TO_REDACT)
