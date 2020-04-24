# Example
`1- kubectl apply -f nginx-dep.yaml`

   deploy nginx server with 3 replicas


`2- kubectl apply -f nginx-dep-svc.yaml`

   Create a service on nodeport which upon
   calling with the UP Address of any  of the
   node in cluster with the 30163, send the
   resquest to any of the pod 

`3 - References`

https://matthewpalmer.net/kubernetes-app-developer/articles/service-kubernetes-example-tutorial.html
https://kubernetes.io/docs/tasks/access-application-cluster/service-access-application-cluster/
