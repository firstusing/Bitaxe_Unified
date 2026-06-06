from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription, SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    PERCENTAGE,
    UnitOfTime,
)

from .const import DOMAIN
from .entity import BitaxeEntity


@dataclass(frozen=True)
class BitaxeSensorDescription(SensorEntityDescription):
    aliases: tuple[str, ...] = ()
    unit: str | None = None


def S(key: str, name: str, aliases: tuple[str, ...], unit: str | None = None, device_class=None, state_class=None, icon: str | None = None) -> BitaxeSensorDescription:
    return BitaxeSensorDescription(
        key=key,
        name=name,
        aliases=aliases,
        unit=unit,
        device_class=device_class,
        state_class=state_class,
        icon=icon,
    )


SENSORS: list[BitaxeSensorDescription] = [
    # Hashrate / performance
    S("hash_rate", "Hash rate", ("hashRate", "hashrate", "currentHashrate", "statistics_hashRate", "statistics_dashboard_hashRate"), "GH/s"),
    S("hash_rate_1m", "Hash rate 1m avg", ("hashRate_1m", "hashRate1m", "hashRate1Min", "hashrate1m", "statistics_hashRate_1m", "statistics_hashRate1m"), "GH/s"),
    S("hash_rate_10m", "Hash rate 10m avg", ("hashRate_10m", "hashRate10m", "hashRate10Min", "hashrate10m", "statistics_hashRate_10m", "statistics_hashRate10m"), "GH/s"),
    S("hash_rate_1h", "Hash rate 1h avg", ("hashRate_1h", "hashRate1h", "hashRate1Hour", "hashrate1h", "statistics_hashRate_1h", "statistics_hashRate1h"), "GH/s"),
    S("asic_1_hash_rate", "ASIC 1 hash rate", ("ASIC_0_hashRate", "asic_0_hashRate", "asic_hashRate", "asic_hashrate", "asic_asic_0_hashRate"), "GH/s"),
    S("expected_hash_rate", "Expected hash rate", ("expectedHashrate", "expectedHashRate", "expectedHashRateGHs", "nominalHashrate"), "GH/s"),
    S("efficiency", "Efficiency", ("efficiency", "efficiencyJTH", "efficiencyJperTH", "jth"), "J/TH"),

    # ASIC / thermal
    S("asic_temperature", "ASIC temperature", ("temp", "asicTemp", "asicTemperature", "asic_temp", "system_temp"), UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
    S("asic_temperature_2", "ASIC temperature 2", ("temp2", "asicTemp2", "asicTemperature2", "asic_temp2", "system_temp2"), UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
    S("vr_temperature", "VR temperature", ("vrTemp", "vrTemperature", "voltageRegulatorTemp", "system_vrTemp"), UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
    S("target_temperature", "Target temperature", ("temptarget", "tempTarget", "targetTemp", "targetTemperature"), UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
    S("overheat_mode", "Overheat mode", ("overheatMode", "overheat_mode", "thermalMode"), None, None, None, "mdi:thermometer-alert"),

    # ASIC config / silicon
    S("asic_frequency", "ASIC frequency", ("frequency", "asicFrequency", "ASICFrequency", "system_frequency"), "MHz"),
    S("asic_core_count", "ASIC core count", ("coreCount", "asicCoreCount", "ASICCoreCount", "cores", "asic_cores"), None),
    S("asic_1_errors", "ASIC 1 errors", ("ASIC_0_errors", "asic_0_errors", "asic_errors", "asic_errorCount", "asic_asic_0_errors"), None, None, SensorStateClass.TOTAL_INCREASING),
    S("error_rate", "Error rate", ("errorRate", "error_rate", "asicErrorRate"), PERCENTAGE),
    S("overclock", "Overclock", ("overclock", "overclockEnabled", "overClock", "overClockEnabled"), None, None, None, "mdi:speedometer"),

    # Power / electrical
    S("power", "Power", ("power", "powerConsumption", "system_power"), UnitOfPower.WATT, SensorDeviceClass.POWER),
    S("current", "Current", ("current", "currentA", "inputCurrent"), UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT),
    S("input_voltage", "Input voltage", ("voltage", "inputVoltage", "inputVoltageMv", "inputVoltageMV"), UnitOfElectricPotential.MILLIVOLT, SensorDeviceClass.VOLTAGE),
    S("nominal_voltage", "Nominal voltage", ("nominalVoltage", "nominal_voltage"), UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE),
    S("core_voltage_target", "Core voltage target", ("coreVoltage", "coreVoltageTarget", "core_voltage", "system_coreVoltage"), UnitOfElectricPotential.MILLIVOLT, SensorDeviceClass.VOLTAGE),
    S("core_voltage_actual", "Core voltage actual", ("coreVoltageActual", "actualCoreVoltage", "coreVoltageMv", "coreVoltageMeasured"), UnitOfElectricPotential.MILLIVOLT, SensorDeviceClass.VOLTAGE),
    S("max_power_limit", "Max power limit", ("maxPower", "maxPowerLimit", "powerLimit", "max_power_limit"), UnitOfPower.WATT, SensorDeviceClass.POWER),

    # Fan
    S("fan_rpm", "Fan RPM", ("fanrpm", "fanRPM", "fan1rpm", "fan1RPM"), "RPM"),
    S("fan_2_rpm", "Fan 2 RPM", ("fan2rpm", "fan2RPM", "fanrpm2", "fanRPM2"), "RPM"),
    S("fan_speed", "Fan speed", ("fanspeed", "fanSpeed", "fan_speed"), PERCENTAGE),
    S("manual_fan_speed", "Manual fan speed", ("manualFanSpeed", "fanSpeedManual", "manual_fanspeed"), PERCENTAGE),
    S("minimum_fan_speed", "Minimum fan speed", ("minFanSpeed", "minimumFanSpeed", "min_fan_speed"), PERCENTAGE),
    S("auto_fan_speed", "Auto fan speed", ("autofanspeed", "autoFanSpeed", "autoFan", "autofan"), None, None, None, "mdi:fan-auto"),

    # Pool / shares / difficulty
    S("shares_accepted", "Shares accepted", ("sharesAccepted", "acceptedShares", "pool_sharesAccepted"), None, None, SensorStateClass.TOTAL_INCREASING),
    S("shares_rejected", "Shares rejected", ("sharesRejected", "rejectedShares", "pool_sharesRejected"), None, None, SensorStateClass.TOTAL_INCREASING),
    S("pool_difficulty", "Pool difficulty", ("poolDifficulty", "pool_difficulty", "difficulty", "pool_diff"), None),
    S("pool_response_time", "Pool response time", ("poolResponseTime", "pool_responseTime", "responseTime", "latency"), "ms"),
    S("blocks_found", "Blocks found", ("blocksFound", "blocks", "foundBlocks"), None, None, SensorStateClass.TOTAL_INCREASING),
    S("best_difficulty_session", "Best difficulty session", ("bestDiff", "bestDifficulty", "bestDiffSession", "bestDifficultySession"), None),
    S("best_difficulty_all_time", "Best difficulty all time", ("bestDiffAllTime", "bestDifficultyAllTime", "bestDiffAlltime", "allTimeBestDiff"), None),
    S("network_difficulty", "Network difficulty", ("networkDifficulty", "network_difficulty", "btcDifficulty"), None),
    S("block_height", "Block height", ("blockHeight", "block_height", "network_blockHeight"), None),

    # Device / network
    S("uptime", "Uptime", ("uptimeSeconds", "uptime", "upTime", "system_uptimeSeconds"), UnitOfTime.SECONDS, SensorDeviceClass.DURATION),
    S("wifi_signal", "WiFi signal", ("wifiRSSI", "wifiRssi", "rssi", "wifiSignal", "wifi_signal"), "dBm", None),
    S("free_heap", "Free heap", ("freeHeap", "heapFree"), "B"),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BitaxeSensor(coordinator, description) for description in SENSORS])


class BitaxeSensor(BitaxeEntity, SensorEntity):
    def __init__(self, coordinator, description: BitaxeSensorDescription) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{coordinator.api.host}_{description.key}"
        self._attr_native_unit_of_measurement = description.unit
        self._attr_device_class = description.device_class
        self._attr_state_class = description.state_class
        self._attr_icon = description.icon

    @property
    def native_value(self):
        flat = self.coordinator.data.get("flat", {})
        for alias in self.entity_description.aliases:
            if alias in flat and flat[alias] is not None:
                return _normalize_value(flat[alias])
        return None

    @property
    def extra_state_attributes(self):
        flat = self.coordinator.data.get("flat", {})
        source_key = next((alias for alias in self.entity_description.aliases if alias in flat and flat[alias] is not None), None)
        return {"source_key": source_key} if source_key else None


def _normalize_value(value: Any):
    if isinstance(value, bool):
        return "On" if value else "Off"
    if isinstance(value, str):
        lowered = value.lower().strip()
        if lowered in {"true", "false"}:
            return "On" if lowered == "true" else "Off"
        # Keep strings like Normal/Enabled as-is, but parse numeric strings.
        try:
            return float(value)
        except ValueError:
            return value
    return value
