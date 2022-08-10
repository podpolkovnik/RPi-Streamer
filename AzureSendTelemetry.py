import os
import time
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=NexCity-Playground.azure-devices.net;DeviceId=Test-Camera-01;SharedAccessKey=OcZRgnQPt8VJI6bWK6QgUC3Gk26ZKqDu0v5fG7A9Ddk="

queue_length = 0
transmitted = 0
timestamp = 0
battery_voltage = 0
rssi = None
gps_coordinates = None
gps_satellites = None

MSG_TXT = '{{"queue-length": {queue_length},\
             "transmitted": {transmitted},\
             "timestamp": {timestamp},\
             "battery-voltage": {battery_voltage},\
             "rssi": {rssi},\
             "gps-coordinates": {gps_coordinates},\
             "gps-satellites": {gps_satellites}}}'


def send_telemetry(client):
    global transmitted

    # This script will send telemetry every 5 minutes
    print("IoT Hub device sending periodic messages")

    client.connect()

    while True:
        timestamp = int(time.time())
        transmitted += 1
        msg_txt_formatted = MSG_TXT.format(queue_length=queue_length,
                                            transmitted=transmitted,
                                            timestamp=timestamp,
                                            battery_voltage=battery_voltage,
                                            rssi=rssi,
                                            gps_coordinates=gps_coordinates,
                                            gps_satellites=gps_satellites)
        message = Message(msg_txt_formatted)

        # Send the message.
        print("Sending message: {}".format(message))
        client.send_message(message)
        print("Message successfully sent")
        time.sleep(300)


def main():
    print("Press Ctrl-C to exit")

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    try:
        send_telemetry(client)
    except KeyboardInterrupt:
        print("IoTHubClient stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        client.shutdown()

if __name__ == '__main__':
    main()

