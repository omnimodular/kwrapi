"""
Kubernetes API ("kwrapi")

TODO: move out environment logic outside the API functions.
"""

import os
from typing import Optional
from requests import PreparedRequest, Request, Session


ENVIRONMENT = "production" if os.path.exists("/run/secrets/kubernetes.io") else "development"
CA_CRT = "/run/secrets/kubernetes.io/serviceaccount/ca.crt"
TOKEN = "/run/secrets/kubernetes.io/serviceaccount/token"
NAMESPACE = "/run/secrets/kubernetes.io/serviceaccount/namespace"


def host() -> str:
    """
    Returns the K8s hostname
    """
    if ENVIRONMENT == "production":
        _ = os.environ["KUBERNETES_SERVICE_HOST"]
    else:
        _ = os.environ.get("KWRAPI_HOST", "127.0.0.1")
    return _


def port() -> int:
    """
    Returns the Kubernetes API port
    """
    if ENVIRONMENT == "production":
        _ = int(os.environ["KUBERNETES_SERVICE_PORT_HTTPS"])
    else:
        _ = int(os.environ.get("KWRAPI_PORT", "8001"))
    return _


def namespace() -> str:
    """
    Returns the Pod namespace.
    """
    if ENVIRONMENT == "production":
        with open(NAMESPACE, encoding="utf-8") as _:
            return _.read()
    else:
        return os.environ.get("KWRAPI_NAMESPACE", "default")


def ca_crt() -> Optional[str]:
    """
    Returns the Kubernetes API CA certificate.
    """
    if ENVIRONMENT == "production":
        with open(CA_CRT, encoding="utf-8") as _:
            return _.read()
    else:
        return None


def token() -> Optional[str]:
    """
    Returns the Kubernetes API secret.

    Use as follows:

        headers = {"Authentication": f"Bearer {kwrapi.token()}"}

    """
    if ENVIRONMENT == "production":
        with open(TOKEN, encoding="utf-8") as _:
            return _.read()
    else:
        return None


def proto() -> str:
    """
    Returns the protocol ("http" or "https") used to connect to the Kubernetes
    control plane.
    """
    return "https" if ENVIRONMENT == "production" else "http"


def get_pod(name) -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/api/v1/namespaces/{namespace()}/pods/{name}"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("GET", url, headers=headers)
    return req.prepare()


def post_pod(body) -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/api/v1/namespaces/{namespace()}/pods"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("POST", url, json=body, headers=headers)
    return req.prepare()


def get_job(name) -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/apis/batch/v1/namespaces/{namespace()}/jobs/{name}"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("GET", url, headers=headers)
    return req.prepare()


def post_job(body) -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/apis/batch/v1/namespaces/{namespace()}/jobs"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("POST", url, json=body, headers=headers)
    return req.prepare()


def get_deployments() -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployments"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("GET", url, headers=headers)
    return req.prepare()


def get_deployment_scale(name):
    """
    TODO: documentation

    ```
    {
      "apiVersion": "autoscaling/v1",
      "kind": "Scale",
      "metadata": {
          "creationTimestamp": "2023-02-09T11:18:59Z",
          "name": "my-app",
          "namespace": "default",
          "resourceVersion": "3489952",
          "uid": "ac767d2a-7315-4972-9062-0808719adf03"
      },
      "spec": {
          "replicas": 2
      },
      "status": {
          "replicas": 2,
          "selector": "app=my-app"
      }
    }
    ```
    """
    url = f"{proto()}://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployment/{name}/scale"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("GET", url, headers=headers)
    return req.prepare()


def set_deployment_scale(name, scale):
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployment/{name}/scale"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    body = {
        "spec": {
            "replicas": scale
        }
    }
    req = Request("POST", url, headers=headers, json=body)
    return req.prepare()


def get_deployment(name) -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployment/{name}"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("GET", url, headers=headers)
    return req.prepare()


def post_deployment(body) -> PreparedRequest:
    """
    TODO: documentation
    """
    url = f"{proto()}://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployments"
    if ENVIRONMENT == "production":
        headers = {"Authorization": f"Bearer {token()}"}
    else:
        headers = None
    req = Request("POST", url, json=body, headers=headers)
    return req.prepare()


def session() -> Session:
    """
    Returns a requests.Session object, initialized to check the server TLS
    certificate against the local CA certificate.
    """
    _ = Session()
    if ENVIRONMENT == "production":
        _.verify = CA_CRT
    return _
