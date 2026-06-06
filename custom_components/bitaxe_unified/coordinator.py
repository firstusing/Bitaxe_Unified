from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BitaxeApi, BitaxeApiError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


OPTIONAL_ENDPOINTS = {
    "system": "system",
    "asic": "asic",
    "pool": "pool",
    "network": "network",
    "statistics": "statistics",
    "statistics_dashboard": "statistics_dashboard",
}


class BitaxeCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api: BitaxeApi, name: str) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{name}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api
        self.device_name = name
        self.optimistic_paused: bool | None = None
        self.endpoint_errors: dict[str, str] = {}

    async def _async_update_data(self) -> dict:
        try:
            info = await self.api.info()
        except BitaxeApiError as err:
            raise UpdateFailed(str(err)) from err

        data: dict[str, dict] = {"info": info or {}}
        self.endpoint_errors = {}

        for name, method_name in OPTIONAL_ENDPOINTS.items():
            try:
                value = await getattr(self.api, method_name)()
                data[name] = value or {}
            except BitaxeApiError as err:
                data[name] = {}
                self.endpoint_errors[name] = str(err)
                _LOGGER.debug("Bitaxe optional endpoint %s unavailable: %s", name, err)

        flat: dict[str, object] = {}
        for endpoint, payload in data.items():
            if not isinstance(payload, dict):
                continue
            # unprefixed values keep compatibility with older entity mapping
            flat.update(_flatten(payload))
            # prefixed values avoid collisions and help with aliases
            flat.update({f"{endpoint}_{k}": v for k, v in _flatten(payload).items()})
        data["flat"] = flat
        data["endpoint_errors"] = dict(self.endpoint_errors)
        return data


def _flatten(value: dict, prefix: str = "") -> dict:
    result = {}
    if not isinstance(value, dict):
        return result
    for key, item in value.items():
        normalized_key = f"{prefix}{key}" if not prefix else f"{prefix}_{key}"
        if isinstance(item, dict):
            result.update(_flatten(item, normalized_key))
        else:
            result[normalized_key] = item
    return result
