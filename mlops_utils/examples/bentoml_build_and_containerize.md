## BentoML Build and Containerize

아래의 예제와 같이, BentoML을 이용해서 모델 서빙을 위한 코드가 build, containerize 될 수 있다.

- bentofile.yaml이 `./modules/services/{model_name}/bentofile.yaml`의 경로에 있다고 가정한다.
- `model_name:model_stage` alias로 containerize가 된다. `model_stage`에 아무 값도 넣지 않으면 `latest`로 설정된다.

```python
import click

from mlops_utils.build.client import (
    bentoml_build,
    bentoml_containerize,
)

@click.command()
@click.option("--model_name", type=str, required=True)
@click.option("--model_stage", type=str, default="")
def bentoml_build_and_containerize(
    model_name: str,
    model_stage: str,
):
    # build and containerize
    model_stage = "latest" if model_stage == "None" else model_stage
    bentoml_build(model_name)
    bentoml_containerize(
        model_name,
        model_stage,
    )

if __name__ == "__main__":
    bentoml_build_and_containerize()
```
