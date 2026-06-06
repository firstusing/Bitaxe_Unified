from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, MANUFACTURER


class BitaxeEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, suffix: str) -> None:
        super().__init__(coordinator)
        self._suffix = suffix
        host = coordinator.api.host
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            manufacturer=MANUFACTURER,
            name=coordinator.device_name,
            configuration_url=f"http://{host}",
        )

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success
