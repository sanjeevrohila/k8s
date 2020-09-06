
###Create configuration (Imperative way)
```
$ kubectl create configmap myconfig --from-literal=key1=val1 --from-literal=key2=val2 --dry-run -o yaml
apiVersion: v1
data:
  key1: val1
  key2: val2
kind: ConfigMap
metadata:
  creationTimestamp: null
  name: myconfig
```
