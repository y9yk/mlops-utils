from google.cloud import secretmanager


def get_secret_str(version: str, project: str, secret: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(
        request={"name": f"projects/{project}/secrets/{secret}/versions/{version}"}
    )
    payload = response.payload.data.decode("UTF-8")
    return payload
