from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from .const import DOMAIN
from .entity import BitaxeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BitaxeMiningBinarySensor(coordinator), BitaxeAutoFanBinarySensor(coordinator)])


class BitaxeMiningBinarySensor(BitaxeEntity, BinarySensorEntity):
    _attr_name = "Mining active"
    _attr_device_class = BinarySensorDeviceClass.RUNNING

    def __init__(self, coordinator):
        super().__init__(coordinator, "mining_active")
        self._attr_unique_id = f"{coordinator.api.host}_mining_active"

    @property
    def is_on(self):
        flat = self.coordinator.data.get("flat", {})
        if "paused" in flat:
            return not bool(flat["paused"])
        if self.coordinator.optimistic_paused is not None:
            return not self.coordinator.optimistic_paused
        hr = flat.get("hashRate")
        return None if hr is None else float(hr) > 0


class BitaxeAutoFanBinarySensor(BitaxeEntity, BinarySensorEntity):
    _attr_name = "Auto fan enabled"

    def __init__(self, coordinator):
        super().__init__(coordinator, "autofan_enabled")
        self._attr_unique_id = f"{coordinator.api.host}_autofan_enabled"

    @property
    def is_on(self):
        value = self.coordinator.data.get("flat", {}).get("autofanspeed")
        return None if value is None else bool(value)
