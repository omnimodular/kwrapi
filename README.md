Kubernetes API boilerplate for Python
=====================================

First define a Deployment:

```python
my_job = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {
        "name": "my-job"
    },
    "spec": {
        "template": {
            "spec": {
                "restartPolicy": "Never",
                "containers": [
                    {
                        "name": "hello",
                        "image": "hello-world:latest"
                    }
                ]
            }
        }
    }
}
```

Second, prepare a request and send it to K8s:

```python
req = kwarpi.post_job(my_job)
with kwarpi.session() as session:
    res = session.send(req) 
    print(res.json())
```


### requirements.txt

```yaml
--find-links https://github.com/omnimodular/kwrapi/releases/download/v0.0.2/kwrapi-0.0.2-py3-none-any.whl 
kwrapi>=0.0.2
```
