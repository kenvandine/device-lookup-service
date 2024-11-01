# Device Lookup Service

Simple web service for storing and querying for configuration values 
based on device serial

## Running the service 

```
python3 app.py
```

## Usage

Query for configuration values:
```
./query SERIAL
```

Adding record for new device serial
```
./add SERIAL LANDSCAPE_ID LANDSCAPE_KEY LANDSCAPE_URL
```
