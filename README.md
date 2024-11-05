# Device Lookup Service

Simple web service for storing and querying for configuration 
based on device serial. Capable of storing configuration values
as well as autoinstall.yaml data for provisioning.

Device serial is expected to be unique, perhaps the value of chassis serial 
in dmidecode which can be found in /sys/class/dmi/id/chassis_serial

## Installation

[![Get it from the Snap Store](https://snapcraft.io/en/dark/install.svg)](https://snapcraft.io/device-lookup-service)

```
sudo snap install device-lookup-service
```

# Device Configuration
Supports storing arbitrary key/value configuration as JSON

## Usage

By default all commands will use the service installed on the localhost. To 
use a remote hosted device-lookup-service set the following environment
variables:

```
export DEVICE_LOOKUP_SERVER=http://somehost
export DEVICE_LOOKUP_PORT=8080
```

Query for configuration values for a given device:
```
device-lookup-service.query SERIAL
```

Query for configuration values for all devices:
```
device-lookup-service.query
```

Adding record for new device serial. You can find a valid configuration at examples/device.json
```
device-lookup-service.add SERIAL INPUT_JSON_FILE
```
This JSON file can contain any valid json

# Device Provisioning (autoinstall.yaml)
Supports storing arbitrary key/value configuration as JSON

## Usage

Retrieve stored autoinstall.yaml for a given device:
```
device-lookup-service.autoinstall SERIAL
```

Adding autoinstall.yaml for new device serial, you can find an valid example at examples/autoinstall.yaml
```
device-lookup-service.add-autoinstall SERIAL AUTOINSTALL_YAML
```
