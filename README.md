# Device Lookup Service

Simple web service for storing and querying for configuration 
based on device serial. Capable of storing configuration values
as well as autoinstall.yaml data for provisioning.

## Running the service 
```
python3 app.py
```

## Installation

[![Get it from the Snap Store](https://snapcraft.io/en/dark/install.svg)](https://snapcraft.io/device-lookup-service)

```
sudo snap install device-lookup-service
```

# Device Configuration
Supports storing arbitrary key/value configuration as JSON

## Usage

Query for configuration values for a given device:
```
./query SERIAL
```

Query for configuration values for all devices:
```
./query
```

Adding record for new device serial
```
./add SERIAL INPUT_JSON_FILE
```
This JSON file can contain any valid json

# Device Provisioning (autoinstall.yaml)
Supports storing arbitrary key/value configuration as JSON

## Usage

Retrieve stored autoinstall.yaml for a given device:
```
./autoinstall SERIAL
```

Adding autoinstall.yaml for new device serial
```
./add-autoinstall SERIAL AUTOINSTALL_YAML
```
