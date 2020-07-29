Get all images in all pods:
```sh
$ for ele in `kubectl get po -o jsonpath='{.items[*].spec.containers[*].image}'`; do echo $ele; done
```
