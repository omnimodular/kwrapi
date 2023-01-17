"""
Kubernetes API ("kwrapi")
"""

import os
from requests import Request, Session

CA_CRT = "/run/secrets/kubernetes.io/serviceaccount/ca.crt"
TOKEN = "/run/secrets/kubernetes.io/serviceaccount/token"
NAMESPACE = "/run/secrets/kubernetes.io/serviceaccount/namespace"

def host() -> str:
    """
    Returns the K8s hostname
    """
    return os.environ["KUBERNETES_SERVICE_HOST"]


def port() -> int:
    """
    Returns the Kubernetes API port
    """
    return int(os.environ["KUBERNETES_SERVICE_PORT_HTTPS"])


def namespace() -> str:
    """
    Returns the Pod namespace.
    """
    with open(NAMESPACE, encoding="utf-8") as _:
        return _.read()


def ca_crt() -> str:
    """
    Returns the Kubernetes API CA certificate.
    """
    with open(CA_CRT, encoding="utf-8") as _:
        return _.read()


def token():
    """
    Returns the Kubernetes API secret.

    Use as follows:

        headers = {"Authentication": f"Bearer {kwrapi.token()}"}

    """
    with open(TOKEN, encoding="utf-8") as _:
        return _.read()


def get_job(name):
    """
    TODO: documentation
    """
    url = f"https://{host()}:{port()}/apis/batch/v1/namespaces/{namespace()}/job/{name}"
    headers = {"Authorization": f"Bearer {token()}"}
    req = Request("GET", url, headers=headers)
    return req.prepare()


def post_job(body):
    """
    TODO: documentation
    """
    url = f"https://{host()}:{port()}/apis/batch/v1/namespaces/{namespace()}/jobs"
    headers = {"Authorization": f"Bearer {token()}"}
    req = Request("POST", url, json=body, headers=headers)
    return req.prepare()


def get_deployment(name):
    """
    TODO: documentation
    """
    url = f"https://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployment/{name}"
    headers = {"Authorization": f"Bearer {token()}"}
    req = Request("GET", url, headers=headers)
    return req.prepare()


def post_deployment(body):
    """
    TODO: documentation
    """
    url = f"https://{host()}:{port()}/apis/apps/v1/namespaces/{namespace()}/deployments"
    headers = {"Authorization": f"Bearer {token()}"}
    req = Request("POST", url, json=body, headers=headers)
    return req.prepare()


def session():
    """
    Returns a requests.Session object, initialized to check the server TLS
    certificate against the local CA certificate.
    """
    _ = Session()
    _.verify = CA_CRT
    return _
