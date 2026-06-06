from __future__ import annotations

from dataclasses import dataclass
from homeassistant.components.button import ButtonEntity, ButtonDeviceClass
from .const import DOMAIN
from .entity import BitaxeEntity


@dataclass(frozen=True)
class ButtonDescription:
    key: str
    name: str
    method: str
    device_class: ButtonDeviceClass | None = None

BUTTONS = [
    ButtonDescription("pause", "Pause mining", "pause"),
    ButtonDescription("resume", "Resume mining", "resume"),
    ButtonDescription("restart", "Restart", "restart", ButtonDeviceClass.RESTART),
    ButtonDescription("identify", "Identify", "identify", ButtonDeviceClass.IDENTIFY),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BitaxeButton(coordinator, description) for description in BUTTONS])


class BitaxeButton(BitaxeEntity, ButtonEntity):
    def __init__(self, coordinator, description: ButtonDescription) -> None:
        super().__init__(coordinator, description.key)
        self._description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{coordinator.api.host}_{description.key}"
        self._attr_device_class = description.device_class

    async def async_press(self) -> None:
        await getattr(self.coordinator.api, self._description.method)()
        if self._description.key == "pause":
            self.coordinator.optimistic_paused = True
        elif self._description.key == "resume":
            self.coordinator.optimistic_paused = False
        await self.coordinator.async_request_refresh()
