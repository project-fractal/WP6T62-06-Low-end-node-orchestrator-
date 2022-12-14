## a low-end opertator for the FRACTAL project

## Features

- Bridges between the IoT Hub and Kubernetes Cluster
- Shows the nodes in CRD format in the Kubernetes Cluster
- Supports any other MQTT broker-based connection

## How to configure

Put the IoT hub credentials in the `config.yaml` file. 
The credentials should be encoded to base64.

## How to build and run
The following instructins assume that you have a running Kubernetes cluster with a local docker registry.

```shell
git clone https://github.com/vahidmohsseni/k8s-low-end-ctrl
cd k8s-low-end-ctrl
cd controller
docker build -t k8s-low-end-ctrl .
docker tag k8s-low-end-ctrl <registry-address>:<registry-port>/k8s-low-end-ctrl
docker push <registry-address>:<registry-port>/k8s-low-end-ctrl
cd ../deploy
# EDIT the image address in the pod.yaml file
# YOU can change the image address by the following command
sed -i 's|image: .*|image: <registry-address>:<registry-port>/k8s-low-end-ctrl|g' pod.yaml
kubectl apply -f namespace.yaml
kubectl apply -f crd.yaml
kubectl apply -f config.yaml
kubectl apply -f rbac.yaml
kubectl apply -f serviceaccount.yaml
kubectl apply -f pod.yaml

```