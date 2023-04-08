## Deploy to Google Cloud Run

BentoML로 생성된 모델 서빙 이미지가 Google Cloud Run에 배포되는 예제는 아래와 같다.

```python
import os
import click
import bentoml

from mlops_utils.utils.secret import get_secret_str
from mlops_utils.build.client import (
    deploy_to_cloud_run,
)


@click.command()
@click.option("--model_name", type=str, required=True)
@click.option("--model_stage", type=str, default="")
@click.option("--gcp_project", type=str, required=True)
@click.option("--gcp_region", type=str, default="asia-northeast3")
@click.option("--gcp_service_port", type=int, default=8080)
def deploy(
    model_name: str,
    model_stage: str,
    gcp_project: str,
    gcp_region: str,
    gcp_service_port: int,
):
    # get model (containerized by bentoml) tag
    model_tag = bentoml.get(f"{model_name}:{model_stage}").tag
    
    # deploy
    deploy_to_cloud_run(
        model_tag.name,
        model_tag.version,
        gcp_project,
        gcp_region,
        gcp_service_port,
    )


if __name__ == "__main__":
    deploy()
