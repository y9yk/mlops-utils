## Getting Secret string from Google Secret Manager

Google Secret Manager를 통해서 관리되는 정보를 가져올 수 있는 예제는 아래와 같다.

```python
import click

from mlops_utils.utils.secret import get_secret_str


@click.command()
@click.option("--version", type=str, required=True, default="latest")
@click.option("--project", type=str, required=True)
@click.option("--secret", type=str, required=True)
def get_secret_str_from_google_secret_manager(version: str, project: str, secret: str) -> None:
    # get secret str
    payload = get_secret_str(version, project, secret)

    # print it
    print(payload, end="")


if __name__ == "__main__":
    get_secret_str_from_google_secret_manager()
```
