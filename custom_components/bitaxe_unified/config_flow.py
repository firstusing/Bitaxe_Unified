from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import BitaxeApi, BitaxeApiError
from .const import DOMAIN


class BitaxeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            name = user_input.get(CONF_NAME) or host
            await self.async_set_unique_id(host.lower())
            self._abort_if_unique_id_configured()
            api = BitaxeApi(async_get_clientsession(self.hass), host)
            try:
                info = await api.info()
                name = user_input.get(CONF_NAME) or info.get("hostname") or info.get("deviceModel") or host
            except BitaxeApiError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=name, data={CONF_HOST: host, CONF_NAME: name})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_NAME): str,
            }),
            errors=errors,
        )
