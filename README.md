# Air Alert Monitor for Home Assistant

This integration monitors air alerts in Ukraine using the alerts.in.ua API and provides a sensor entity that can be used in automations to control devices like the Xiaomi Aquara Gateway LED.

## Features

- Monitors air alerts in any configurable region in Ukraine in real-time
- Provides a sensor entity that can be used in automations
- Updates status every minute (configurable)
- Provides detailed alert information as sensor attributes

## Installation

### Method 1: HACS (Recommended)

[HACS (Home Assistant Community Store)](https://hacs.xyz/) provides an easy way to install and update custom integrations.

1. Make sure HACS is installed in your Home Assistant instance.
2. Go to HACS → Integrations → ⋮ (top right) → Custom repositories
3. Add the URL `https://github.com/tunforjob/air_alert` with category `Integration`
4. Click `ADD`
5. Search for "Air Alert" in HACS → Integrations
6. Click `INSTALL`
7. Restart Home Assistant

**Note:** If you encounter an error about missing manifest.json, ensure your repository has the correct structure with the manifest.json file in the `custom_components/air_alert/` directory.

### Method 2: Manual Installation

1. Copy the `custom_components/air_alert` directory to your Home Assistant custom components directory:
   ```
   /config/custom_components/air_alert/
   ```

2. Create the directory structure if it doesn't exist:
   ```bash
   mkdir -p /config/custom_components/air_alert/
   ```

### Method 2: Installation from GitHub

1. Navigate to your Home Assistant configuration directory:
   ```bash
   cd /config
   ```

2. If you don't have a `custom_components` directory, create one:
   ```bash
   mkdir -p custom_components
   ```

3. Clone the repository directly into your custom_components directory:
   ```bash
   git clone https://github.com/your-username/air_alert.git custom_components/air_alert
   ```
   
   Or download and extract the ZIP file:
   ```bash
   wget https://github.com/your-username/air_alert/archive/main.zip
   unzip main.zip
   mv air_alert-main/custom_components/air_alert custom_components/
   rm -rf air_alert-main main.zip
   ```

### Установка из GitHub (Russian Instructions)

#### Метод 1: HACS (Рекомендуется)

[HACS (Home Assistant Community Store)](https://hacs.xyz/) предоставляет простой способ установки и обновления пользовательских интеграций.

1. Убедитесь, что HACS установлен в вашем экземпляре Home Assistant.
2. Перейдите в HACS → Интеграции → ⋮ (вверху справа) → Пользовательские репозитории
3. Добавьте URL `https://github.com/your-username/air_alert` с категорией `Integration`
4. Нажмите `ДОБАВИТЬ`
5. Найдите "Air Alert" в HACS → Интеграции
6. Нажмите `УСТАНОВИТЬ`
7. Перезагрузите Home Assistant

#### Метод 2: Ручная установка

1. Перейдите в директорию конфигурации Home Assistant:
   ```bash
   cd /config
   ```

2. Если у вас нет директории `custom_components`, создайте её:
   ```bash
   mkdir -p custom_components
   ```

3. Клонируйте репозиторий прямо в директорию custom_components:
   ```bash
   git clone https://github.com/your-username/air_alert.git custom_components/air_alert
   ```
   
   Или скачайте и распакуйте ZIP-файл:
   ```bash
   wget https://github.com/your-username/air_alert/archive/main.zip
   unzip main.zip
   mv air_alert-main/custom_components/air_alert custom_components/
   rm -rf air_alert-main main.zip
   ```

### Configuration

1. Install the required Python package:
   ```bash
   pip install alerts_in_ua
   ```

2. Add the following to your Home Assistant `configuration.yaml`:
   ```yaml
   sensor:
     - platform: air_alert
       api_token: "YOUR_API_TOKEN"  # Replace with your actual token from alerts.in.ua
       region_type: "location_oblast"  # Type of region to monitor
       region_name: "Харківська область"  # Name of the region to monitor
       scan_interval: 60  # Check every 60 seconds
   ```

3. Obtain an API token from [alerts.in.ua](https://alerts.in.ua/api-request)

4. Restart Home Assistant

### Конфигурация (Russian Configuration)

1. Установите необходимый Python пакет:
   ```bash
   pip install alerts_in_ua
   ```

2. Добавьте следующее в ваш файл `configuration.yaml` в Home Assistant:
   ```yaml
   sensor:
     - platform: air_alert
       api_token: "ВАШ_API_ТОКЕН"  # Замените на ваш токен с alerts.in.ua
       region_type: "location_oblast"  # Тип региона для мониторинга
       region_name: "Харківська область"  # Название региона для мониторинга
       scan_interval: 60  # Проверять каждые 60 секунд
   ```

3. Получите API токен на сайте [alerts.in.ua](https://alerts.in.ua/api-request)

4. Перезагрузите Home Assistant

## Configuration Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|  
| `api_token` | Your API token from alerts.in.ua | Yes | - |
| `region_type` | Type of region to monitor (e.g., location_oblast, location_raion) | No | `location_oblast` |
| `region_name` | Name of the region to monitor (e.g., Харківська область) | No | `Харківська область` |
| `name` | Name for the sensor entity | No | `Air Alert` |
| `scan_interval` | How often to check for alerts (in seconds) | No | 60 |

## Creating an Automation for Xiaomi Aquara Gateway LED

To control your Xiaomi Aquara Gateway LED (Light_34ce00fa6b10) based on the air alert status, add the following automation to your Home Assistant `automations.yaml` file:

```yaml
- alias: "Air Alert - Control Xiaomi Aquara Gateway LED"
  description: "Turn on red light when air alert is active in the monitored region, turn off when clear"
  trigger:
    - platform: state
      entity_id: sensor.air_alert
  action:
    - choose:
        # When alert is active, turn on red light
        - conditions:
            - condition: state
              entity_id: sensor.air_alert
              state: "Alert"
          sequence:
            - service: light.turn_on
              target:
                entity_id: light.light_34ce00fa6b10
              data:
                rgb_color: [255, 0, 0]  # Red color
                brightness: 255  # Full brightness
        # When alert is clear, turn off light
        - conditions:
            - condition: state
              entity_id: sensor.air_alert
              state: "Clear"
          sequence:
            - service: light.turn_off
              target:
                entity_id: light.light_34ce00fa6b10
      # Default action if none of the conditions match
      default: []
  mode: single
```

You can also create this automation through the Home Assistant UI by going to **Configuration** > **Automations & Scenes** > **Create Automation**.

### Создание автоматизации для Xiaomi Aquara Gateway LED (Russian Example)

Чтобы управлять светодиодом Xiaomi Aquara Gateway (Light_34ce00fa6b10) на основе статуса воздушной тревоги, добавьте следующую автоматизацию в файл `automations.yaml` вашего Home Assistant:

```yaml
- alias: "Воздушная тревога - Управление светодиодом Xiaomi Aquara Gateway"
  description: "Включить красный свет при активной воздушной тревоге, выключить при отсутствии тревоги"
  trigger:
    - platform: state
      entity_id: sensor.air_alert
  action:
    - choose:
        # Когда тревога активна, включить красный свет
        - conditions:
            - condition: state
              entity_id: sensor.air_alert
              state: "Alert"
          sequence:
            - service: light.turn_on
              target:
                entity_id: light.light_34ce00fa6b10
              data:
                rgb_color: [255, 0, 0]  # Красный цвет
                brightness: 255  # Полная яркость
        # Когда тревога отсутствует, выключить свет
        - conditions:
            - condition: state
              entity_id: sensor.air_alert
              state: "Clear"
          sequence:
            - service: light.turn_off
              target:
                entity_id: light.light_34ce00fa6b10
      default: []
  mode: single
```

Эта автоматизация будет:

1. Включать светодиод Xiaomi Aquara Gateway красным цветом при активной тревоге
2. Выключать светодиод при отсутствии тревоги

## Usage

Once installed and configured, the integration will automatically:
1. Check for air alerts in the Kharkiv region every minute
2. Provide a sensor entity with the current alert status

The automation (if added) will then:
1. Turn the Xiaomi Aquara Gateway LED red when an alert is active
2. Turn the LED off when there are no active alerts

The sensor entity will be available in Home Assistant as `sensor.air_alert` with the following states:
- `Alert`: When there's an active alert in the monitored region
- `Clear`: When there are no active alerts
- `Error`: When there's an error connecting to the API

## Troubleshooting

- Check Home Assistant logs for any error messages
- Verify your API token is correct
- Ensure the Xiaomi Aquara Gateway is properly set up in Home Assistant
- Check that the entity ID for the light is correct
