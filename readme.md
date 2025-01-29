# HumonSens

HumonSens is a Python-based project for managing the connection and reading data from a flexible capacitive sensor via the serial port.

## Table of Contents
- [HumonSens](#humonsens)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Data Protocol](#data-protocol)
    - [Log File](#log-file)
    - [get\_port méthode](#get_port-méthode)
    - [working with output data](#working-with-output-data)
    - [Example Output](#example-output)
  - [Contributors](#contributors)
  - [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/vinckbooms/humonsens.git
    cd humonsens
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Edit the `humonsens.ini` file to configure the sensor and logging parameters:

```ini
[SENSOR]
port = COM8
baudrate = 9600
timeout = 1

[LOGGING]
log_file = humonsens.log
log_level = INFO
log_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Usage

To use the HumonSens library in your Python script, follow these steps:

```python
from humonsens import HumonSens

# Initialize the HumonSens object
humonsens = HumonSens()

# Run the sensor reading routine
measures = humonsens.run()

# Print the measures
for key, value in measures.items():
    print(f"{key}: {value}")
```

### Data Protocol

Currently, values are all floats. They are sent in a string, formatted as JSON. For example:

```json
{"ID":"sensor1","F":10000,"temp":21.3,"rh":52.3,"cap":12345}
```
The data to be transferred:

| Name | Type  | Size |
|------|-------|------|
| cap  | int   | 0-4096 |
| freq | int   | 0 - 10^6 |
| ID   | str   | (no limit specified) |
| Temp | float | -50-100 |
| RH   | float | 0-150 (due to use of SHT-31 which sometimes sends values > 100) |

Drummer / follower architecture; Pi sends the command, then waits for a line result from the sensor in JSON.

- **PI**: `SX {frequency:int}\n` -> Sensor
- **Sensor**: `{JSON}\n` -> PI

The sensor might send other text over serial; only the last line is kept and parsed into JSON.

### Log File

The log file specified in the configuration will contain detailed information about the sensor readings and the operation of the script. Ensure that the log file path is correctly set in the `humonsens.ini` file to avoid any issues during execution.

### get_port méthode

```python
for port in humonsens.get_ports():
    print(port)
```

### working with output data

```python
# Valeur recue: {'ID': 'dryCheck_1', 'cap': 22, 'freq': 10000, 'temp': 25, 'RH': 33, 'asked_frequency': 10000}
for key, value in measures.items():
    print(f"{key}: {value}")
```

### Example Output

Here is an example of the output you can expect from the `humonsens.py` script:

```log
2025-01-28 16:53:53,577 - root - INFO - Configuration du capteur HumonSens V2.0 .
2025-01-28 16:53:54,181 - root - INFO - Sleep count: 1
2025-01-28 16:53:54,181 - root - INFO - Read line: {"ID":"dryCheck_1","cap":15,"freq":10000,"temp":25,"RH":33}
2025-01-28 16:53:54,182 - root - INFO - Valeur recue: 15
2025-01-28 16:53:54,183 - root - INFO - Connexion série fermée.
2025-01-28 16:54:29,594 - root - INFO - Configuration du capteur HumonSens V2.0 .
2025-01-28 16:54:30,197 - root - INFO - Sleep count: 1
2025-01-28 16:54:30,197 - root - INFO - Read line: {"ID":"dryCheck_1","cap":18,"freq":10000,"temp":25,"RH":33}
2025-01-28 16:54:30,198 - root - INFO - Valeur recue: {'ID': 'dryCheck_1', 'cap': 18, 'freq': 10000, 'temp': 25, 'RH': 33, 'asked_frequency': 10000}
2025-01-28 16:54:30,198 - root - INFO - Connexion série fermée.
2025-01-28 16:55:32,402 - root - INFO - Configuration du capteur HumonSens V2.0 .
2025-01-28 16:55:33,005 - root - INFO - Sleep count: 1
2025-01-28 16:55:33,006 - root - INFO - Read line: {"ID":"dryCheck_1","cap":22,"freq":10000,"temp":25,"RH":33}
2025-01-28 16:55:33,006 - root - INFO - Valeur recue: {'ID': 'dryCheck_1', 'cap': 22, 'freq': 10000, 'temp': 25, 'RH': 33, 'asked_frequency': 10000}
2025-01-28 16:55:33,007 - root - INFO - Connexion série fermée.
2025-01-28 16:56:53,011 - root - INFO - Configuration du capteur HumonSens V2.0 .
2025-01-28 16:56:53,614 - root - INFO - Sleep count: 1
2025-01-28 16:56:53,615 - root - INFO - Read line: {"ID":"dryCheck_1","cap":22,"freq":10000,"temp":25,"RH":34}
2025-01-28 16:56:53,615 - root - INFO - Valeur recue: {'ID': 'dryCheck_1', 'cap': 22, 'freq': 10000, 'temp': 25, 'RH': 34, 'asked_frequency': 10000}
2025-01-28 16:56:53,616 - root - INFO - Connexion série fermée.
```

This output shows the timestamp, the name of the logger, the log level, and the JSON-formatted sensor data.

Here is an example of the output you can expect from the `humonsens.py` script:

```sh
2023-10-01 12:00:00,000 - humonsens - INFO - {"ID":"sensor1","F":10000,"temp":21.3,"rh":52.3,"cap":12345}
2023-10-01 12:00:01,000 - humonsens - INFO - {"ID":"sensor1","F":10001,"temp":21.4,"rh":52.4,"cap":12346}
2023-10-01 12:00:02,000 - humonsens - INFO - {"ID":"sensor1","F":10002,"temp":21.5,"rh":52.5,"cap":12347}
```

This output shows the timestamp, the name of the logger, the log level, and the JSON-formatted sensor data.

## Contributors

- Samuel Dubois
- Mart Willocx
- Mathieu Vinckbooms

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
