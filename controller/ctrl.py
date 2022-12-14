# system imports
import kopf
import pykube
import os
import logging
from azure.iot.hub import IoTHubRegistryManager

# local imports
from models import LowEnd

CONNECTION_STRING = os.getenv("IOTHUB_CREDENTIALS")

KUBE_CONFIG = pykube.KubeConfig.from_env()
NAMESPACE = "low-end-ctrl"

logger = logging.getLogger(__name__)

@kopf.on.startup()
def init_crds(**_):
    # remove all current crds
    _delete_objects()
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        devices = registry_manager.get_devices(1000)
        for device in devices:
            if device.device_id.startswith("fractal-node-"):
                # get the twin of a device
                twin = registry_manager.get_twin(device.device_id)
                device_id = twin.device_id
                connection_state = twin.connection_state
                _create_object(device_id, connection_state)
    except Exception as e:
        logger.error("Error: %s", e)
        exit(1)


@kopf.on.create("fractal-cluster.eu", "v1", "lowends")
def create_fn(name, spec, **_):
    # get the object 
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        device_id = spec["deviceId"]
        twin = registry_manager.get_twin(device_id)
        reported_state = twin.properties.reported
        desired_state = twin.properties.desired
        _update_object(name, device_id, twin.connection_state, reported_state, desired_state)
    except Exception as e:
        logger.error("Error: %s", e)


@kopf.timer("fractal-cluster.eu", "v1", "lowends", interval=20, initial_delay=10)
def timer_fn(**_):
    logger.warn("The timer is ticking.")
    logger.warn("Implment this function in production.")


@kopf.on.update("fractal-cluster.eu", "v1", "lowends")
def update_fn(name, spec, **_):
    logger.warn(f"The object:{name} is updated.")
    logger.warn("Implment this function in production.")


@kopf.on.cleanup()
def cleanup(**_):
    logger.debug("cleanup")

    logger.warning("deleting all objects")
    _delete_objects()


def _create_object(device_id, connection_state):
    api = pykube.HTTPClient(KUBE_CONFIG)

    # create a new lowend object
    lowend = LowEnd(api, {
        "apiVersion": "fractal-cluster.eu/v1",
        "kind": "LowEnd",
        "metadata": {
            "generateName": "low-end-",
            "namespace": NAMESPACE,
        },
        "spec": {
            "deviceId": device_id,
            "connectionState": connection_state,
        }
    })

    # create the lowend object
    lowend.create()

def _update_object(name, device_id, connection_state, reported_state, desired_state):
    logger.debug("updating object: ", device_id, connection_state)
    logger.debug("reported state: ", reported_state)
    last_reported_updated = reported_state["$metadata"]["$lastUpdated"]
    last_reported = 0 if reported_state.get("data", None) is None else reported_state["data"]["led_state"]
    logger.debug("desired state: ", desired_state)
    last_desired_updated = desired_state["$metadata"]["$lastUpdated"]
    last_desired = 0 if desired_state.get("data", None) is None else desired_state["data"]["led_state"]
    api = pykube.HTTPClient(KUBE_CONFIG)
    lowend = LowEnd.objects(api).filter(namespace=NAMESPACE).get_by_name(name)
    le = LowEnd(api, lowend.obj)
    le.obj["spec"]["connectionState"] = connection_state
    le.obj["spec"]["desiredState"] = {"state": last_desired, "lastUpdated": last_desired_updated}
    le.obj["spec"]["reportedState"] = {"state": last_reported, "lastUpdated": last_reported_updated}

    le.update()

    # lowend.patch({"spec":{"connectionState": "Connected"}})

def _delete_objects():
    api = pykube.HTTPClient(KUBE_CONFIG)
    lowends = LowEnd.objects(api).filter(namespace=NAMESPACE)
    logger.debug("deleting objects ...")
    for lowend in lowends:
        lowend.delete()
        logger.debug("object deleted")
