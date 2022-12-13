import sys, time

from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult, Twin



def iothub_devicemethod_sample_run():
    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)

        print ( "" )
        print ( "Invoking device to reboot..." )

        # Call the direct method.
        # deviceMethod = CloudToDeviceMethod(method_name=METHOD_NAME, payload=METHOD_PAYLOAD)
        # response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)
        # get the list of devices
        devices = registry_manager.get_devices(1000)

        # print devices
        for device in devices:
            print(device.device_id)
        
        # get the twin of a device
        twin = registry_manager.get_twin("fractal-node-904ADF13C9AD3DE1FC48EB3F731BD00D")
        print(twin.properties)


        print ( "" )
        print ( "Successfully invoked the device to reboot." )

        print ( "" )


    except Exception as ex:
        print ( "" )
        print ( "Unexpected error {0}".format(ex) )
        return
    except KeyboardInterrupt:
        print ( "" )
        print ( "IoTHubDeviceMethod sample stopped" )

if __name__ == '__main__':
    print ( "Starting the IoT Hub Service Client DeviceManagement Python sample..." )
    print ( "    Connection string = {0}".format(CONNECTION_STRING) )

    iothub_devicemethod_sample_run()
