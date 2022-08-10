import sys
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import Twin, TwinProperties

CONNECTION_STRING = "HostName=NexCity-Playground.azure-devices.net;DeviceId=Test-Camera-01;SharedAccessKey=OcZRgnQPt8VJI6bWK6QgUC3Gk26ZKqDu0v5fG7A9Ddk="
DEVICE_ID = "rpicam-starvis-small"
MODULE_ID = "test-module"

try:
    # RegistryManager
    iothub_registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

    module_twin = iothub_registry_manager.get_module_twin(DEVICE_ID, MODULE_ID)
    print ( "" )
    print ( "Module twin properties before update    :" )
    print ( "{0}".format(module_twin.properties) )

    # Update twin
    twin_patch = Twin()
    twin_patch.properties = TwinProperties(desired={"telemetryInterval": 122})
    updated_module_twin = iothub_registry_manager.update_module_twin(
        DEVICE_ID, MODULE_ID, twin_patch, module_twin.etag
    )
    print ( "" )
    print ( "Module twin properties after update     :" )
    print ( "{0}".format(updated_module_twin.properties) )

except Exception as ex:
    print ( "Unexpected error {0}".format(ex) )
except KeyboardInterrupt:
    print ( "IoTHubRegistryManager sample stopped" )

