from pykube.objects import NamespacedAPIObject

class LowEnd(NamespacedAPIObject):
    version = "fractal-cluster.eu/v1"
    endpoint = "lowends"
    kind = "LowEnd"
