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
