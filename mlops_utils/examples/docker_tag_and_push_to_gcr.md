## Tag and Push Docker Image to Google Cloud Registry

생성된 이미지를 GCR로 푸시할 수 있는 예제는 아래와 같다.

- GCR에 푸시되는 이미지 이름은 `gcr.io/{GCP_PROJECT_ID}/{MODEL_NAME:MODEL_STAGE}` 이다.

```python
import click
import bentoml

from mlops_utils.utils.secret import get_secret_str
from mlops_utils.build.client import (
    docker_tag_to_image,
    docker_push_to_gcr,
)


@click.command()
@click.option("--model_name", type=str, required=True)
@click.option("--model_stage", type=str, default="")
@click.option("--gcp_project", type=str, required=True)
def docker_tag_and_push_to_gcr(
    model_name: str,
    model_stage: str,
    gcp_project: str,
):
    # get model (containerized by bentoml) tag
    model_tag = bentoml.get(f"{model_name}:{model_stage}").tag
    
    # docker tag and push
    docker_tag_to_image(model_tag.name, model_tag.version, gcp_project)
    docker_push_to_gcr(model_tag.name, model_tag.version, gcp_project)


if __name__ == "__main__":
    docker_tag_and_push_to_gcr()
