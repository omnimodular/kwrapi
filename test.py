import kwrapi

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

req = kwrapi.post_job(my_job)
with kwrapi.session() as session:
    res = session.send(req)
    res.raise_for_status()
    print(res.json())
