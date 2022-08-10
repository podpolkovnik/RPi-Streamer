import time
from azure.iot.device import IoTHubModuleClient
import json


CONNECTION_STRING = "HostName=NexCity-Playground.azure-devices.net;DeviceId=Test-Camera-01;SharedAccessKey=OcZRgnQPt8VJI6bWK6QgUC3Gk26ZKqDu0v5fG7A9Ddk="


def twin_patch_handler(twin_patch):
    print("")
    print("Twin desired properties patch received:")
    print(twin_patch)
    json.dump(twin_patch, 'twin_patch.json', indent=4)


def main():
    print ("Starting the IoT Hub Python sample...")
    client = IoTHubModuleClient.create_from_connection_string(CONNECTION_STRING)

    print ("Waiting for commands, press Ctrl-C to exit")
    try:
        # Attach the handler to the client
        client.on_twin_desired_properties_patch_received = twin_patch_handler

        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print("IoTHubModuleClient sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()

if __name__ == '__main__':
    main()

