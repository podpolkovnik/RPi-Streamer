# RPi-Streamer

## Install necessarry libraries
```console
pip3 install azure-iot-device
pip3 install watchdog

```
## Azure scheme
![alt text](https://github.com/podpolkovnik/RPi-Streamer/blob/main/azure_scheme.jpg)

## Usage
First, run the 'ReceiveModuleTwinDesiredPropertiesPatch.py' to get the configuration file from the server:
```console
python3 ReceiveModuleTwinDesiredPropertiesPatch.py

```
Then run the 'Streamer.py' to start the stream:
```console
python3 Streamer.py

```
