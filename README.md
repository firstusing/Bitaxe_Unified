# Bitaxe Unified for Home Assistant

Native custom integration for Bitaxe / AxeOS / ESP-Miner devices.

## Features

- Local polling via AxeOS REST API
- Multiple Bitaxe devices: add each miner once via UI
- Sensors: hashrate, power, voltage, current, ASIC temperature, VR temperature, fan RPM, fan speed, uptime, shares, best diff, heap, frequency, core voltage, temperature target
- Buttons: pause mining, resume mining, restart, identify
- Switches: mining on/off, auto fan on/off
- Numbers: fan speed, temperature target, ASIC frequency, core voltage

The integration uses the ESP-Miner AxeOS API endpoints documented in the official repository: `/api/system/info`, `/api/system/asic`, `/api/system/pause`, `/api/system/resume`, `/api/system/restart`, `/api/system/identify` and `PATCH /api/system`.

## Installation

### Manual

1. Copy `custom_components/bitaxe_unified` into your Home Assistant `config/custom_components/` folder.
2. Restart Home Assistant.
3. Go to **Settings → Devices & services → Add integration → Bitaxe Unified**.
4. Add each Bitaxe by IP/hostname.

### HACS custom repository

After pushing this folder to GitHub:

1. HACS → Integrations → three-dot menu → Custom repositories.
2. Add your repository URL.
3. Category: Integration.
4. Install **Bitaxe Unified**.

## Temperature automation example

Pause any Bitaxe above 70 °C for 2 minutes:

```yaml
alias: Bitaxe pause on high temperature
mode: parallel
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.bitaxe_1_asic_temperature
      - sensor.bitaxe_2_asic_temperature
      - sensor.bitaxe_3_asic_temperature
      - sensor.bitaxe_4_asic_temperature
    above: 70
    for: "00:02:00"
action:
  - service: switch.turn_off
    target:
      device_id: "{{ device_id(trigger.entity_id) }}"
```

Resume under 60 °C after 10 minutes:

```yaml
alias: Bitaxe resume after cooldown
mode: parallel
trigger:
  - platform: numeric_state
    entity_id:
      - sensor.bitaxe_1_asic_temperature
      - sensor.bitaxe_2_asic_temperature
      - sensor.bitaxe_3_asic_temperature
      - sensor.bitaxe_4_asic_temperature
    below: 60
    for: "00:10:00"
action:
  - service: switch.turn_on
    target:
      device_id: "{{ device_id(trigger.entity_id) }}"
```

## Notes

- Frequency and voltage ranges are intentionally broad. Adjust in `number.py` for your specific Bitaxe model.
- The mining switch uses `/pause` and `/resume`. If your firmware does not report a `paused` field, state is inferred optimistically or from hashrate.
- First version: no WebSocket/live log support yet.
