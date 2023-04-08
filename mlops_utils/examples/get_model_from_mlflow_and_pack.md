## Getting Model from MLflow and Packing it

MLflow에 저장된 모델 아티팩트를 가져와서 BentoML에서 사용할 수 있도록 Packing하는 예제는 아래와 같다.

MLflow 서버는 인증되어야 사용할 수 있다고 가정한다. 때문에 아래 환경 변수가 미리 셋업되어 있어야 한다.

- MLFLOW_TRACKING_USERNAME: 사용자아이디
- MLFLOW_TRACKING_PASSWORD: 비밀번호
- MLFLOW_TRACKING_URI: MLflow 서버 주소

```python
import os
import click
import bentoml

from mlops_utils.utils.secret import get_secret_str
from mlops_utils.utils.mlflow_utils import fetch_logged_info


def set_env(gcp_project: str):
    version = "latest"
    os.environ["MLFLOW_TRACKING_USERNAME"] = get_secret_str(
        version=version,
        project=gcp_project,
        secret="mlflow_tracking_username",
    )
    os.environ["MLFLOW_TRACKING_PASSWORD"] = get_secret_str(
        version=version,
        project=gcp_project,
        secret="mlflow_tracking_password",
    )
    os.environ["MLFLOW_TRACKING_URI"] = get_secret_str(
        version=version,
        project=gcp_project,
        secret="mlflow_tracking_uri",
    )


@click.command()
@click.option("--model_name", type=str, required=True)
@click.option("--model_stage", type=str, default="")
@click.option("--gcp_project", type=str, required=True)
def get_model_from_mlflow_and_pack(model_name: str, model_stage: str, gcp_project: str):
    # setting mlflow connection environment
    set_env(gcp_project=gcp_project)
    
    # fetch model info from mlflow
    model_stage = None if model_stage == "None" else model_stage
    model_info = fetch_logged_info(model_name, model_stage)

    # import fetched model using bentoml
    bentoml.mlflow.import_model(
        model_name,
        model_uri=model_info.get("artifact_uri"),
    )


if __name__ == "__main__":
    get_model_from_mlflow_and_pack()
```
