echo "Creating namespace"
kubectl create namespace graymatter

echo "Adding site conf"
kubectl delete secret -n graymatter config
kubectl create secret -n graymatter generic config --from-file=conf=config.json

echo "Adding elasticsearch conf"
kubectl delete secret -n graymatter es-secret
kubectl create secret -n graymatter generic es-secret --from-file=es_conf=secrets/elasticsearch.json

echo "Deploying frontend service"
kubectl create -f gce-service.yaml

echo "Deploying server"
kubectl create -f gce-frontend.yaml

#echo "label a node as ES capable"
#kubectl label nodes gke-servicex-default-pool-d4908f66-xmc6 es=capable
