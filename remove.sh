rm -rf /var/lib/ambari-server/resources/stacks/HDP/2.2/services/jupyter-service
rm -rf /home/jupyter

#Set Ambari username/password, and cluster name here
CLUSTER=dev
USER=admin
PASS=admin
SERVICE=JUPYTER
HOST=localhost:8080

# Stop service
curl -u $USER:$PASS -i -H 'X-Requested-By: ambari' -X PUT -d \
  '{"RequestInfo": {"context" :"Stop '"$1"' via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' \
  http://$HOST/api/v1/clusters/$CLUSTER/services/$SERVICE
# Remove service from registry
curl -u $USER:$PASS -i -H 'X-Requested-By: ambari' -X DELETE http://$HOST/api/v1/clusters/$CLUSTER/services/$SERVICE

#Remove Python2.7
rm -rf /usr/local/lib/python2.7
rm /usr/local/bin/python2.7
