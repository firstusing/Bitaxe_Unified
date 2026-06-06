from __future__ import annotations

from dataclasses import dataclass
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from .const import DOMAIN
from .entity import BitaxeEntity


@dataclass(frozen=True)
class NumberDescription:
    key: str
    name: str
    unit: str | None
    native_min: float
    native_max: float
    native_step: float

NUMBERS = [
    NumberDescription("fanspeed", "Fan speed", PERCENTAGE, 0, 100, 1),
    NumberDescription("temptarget", "Temperature target", UnitOfTemperature.CELSIUS, 40, 90, 1),
    NumberDescription("frequency", "ASIC frequency", "MHz", 100, 1000, 1),
    NumberDescription("coreVoltage", "Core voltage", "mV", 800, 1500, 1),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BitaxeNumber(coordinator, description) for description in NUMBERS])


class BitaxeNumber(BitaxeEntity, NumberEntity):
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, description: NumberDescription) -> None:
        super().__init__(coordinator, description.key)
        self._description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{coordinator.api.host}_{description.key}_number"
        self._attr_native_unit_of_measurement = description.unit
        self._attr_native_min_value = description.native_min
        self._attr_native_max_value = description.native_max
        self._attr_native_step = description.native_step

    @property
    def native_value(self):
        flat = self.coordinator.data.get("flat", {})
        value = flat.get(self._description.key)
        if value is None:
            value = flat.get(f"asic_{self._description.key}")
        return value

    async def async_set_native_value(self, value: float) -> None:
        key = self._description.key
        payload = {key: int(value) if float(value).is_integer() else value}
        await self.coordinator.api.patch_system(payload)
        await self.coordinator.async_request_refresh()
