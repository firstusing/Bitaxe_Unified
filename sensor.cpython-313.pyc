from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .entity import BitaxeEntity


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BitaxeMiningSwitch(coordinator), BitaxeAutoFanSwitch(coordinator)])


class BitaxeMiningSwitch(BitaxeEntity, SwitchEntity):
    _attr_name = "Mining"

    def __init__(self, coordinator):
        super().__init__(coordinator, "mining")
        self._attr_unique_id = f"{coordinator.api.host}_mining"

    @property
    def is_on(self):
        flat = self.coordinator.data.get("flat", {})
        if "paused" in flat:
            return not bool(flat["paused"])
        if self.coordinator.optimistic_paused is not None:
            return not self.coordinator.optimistic_paused
        hr = flat.get("hashRate")
        return None if hr is None else float(hr) > 0

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.resume()
        self.coordinator.optimistic_paused = False
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.pause()
        self.coordinator.optimistic_paused = True
        await self.coordinator.async_request_refresh()


class BitaxeAutoFanSwitch(BitaxeEntity, SwitchEntity):
    _attr_name = "Auto fan"

    def __init__(self, coordinator):
        super().__init__(coordinator, "autofan")
        self._attr_unique_id = f"{coordinator.api.host}_autofan"

    @property
    def is_on(self):
        value = self.coordinator.data.get("flat", {}).get("autofanspeed")
        return None if value is None else bool(value)

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.patch_system({"autofanspeed": 1})
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.patch_system({"autofanspeed": 0})
        await self.coordinator.async_request_refresh()
