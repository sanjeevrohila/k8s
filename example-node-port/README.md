# Example
`1- Deploy pods with 3 replicasets`
```
kubectl apply -f nginx-dep.yaml
```


`2- Deploy Service for the deployed pods where nginx servers running`
```
kubectl apply -f nginx-dep-svc.yaml
```

Create a service on nodeport which upon
calling with the UP Address of any  of the
node in cluster with the 30163, send the
resquest to any of the pod 

`3 - References`

https://matthewpalmer.net/kubernetes-app-developer/articles/service-kubernetes-example-tutorial.html
https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/

`4 - Check the deployment`
kubectl get deployment

```
ubuntu@k8s-master:~$ kubectl get deployment
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           23h
```

`5 - describe deployment`

```
ubuntu@k8s-master:~$ kubectl describe deployment nginx-deployment
Name:                   nginx-deployment
Namespace:              default
CreationTimestamp:      Thu, 23 Apr 2020 11:42:31 -0700
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=nginx-flask-application,tier=backend,track=stable
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=nginx-flask-application
           tier=backend
           track=stable
  Containers:
   flask-container:
    Image:        nginx
    Port:         80/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   nginx-deployment-6dd686cd46 (3/3 replicas created)
Events:          <none>
```
