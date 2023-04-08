# mlops-utils

모델 서빙을 위한 유틸리티들을 제공합니다.

아래의 기능들을 제공합니다.
  
- [MLflow](https://mlflow.org/)에서 학습된 모델을 가져올 수 있습니다.
- [BentoML](https://www.bentoml.com/)을 이용해서 빌드, 컨테이너화를 할 수 있습니다.
- [Google Cloud Registry](https://cloud.google.com/container-registry)로 해당 이미지를 푸시할 수 있습니다.
- [Google Cloud Run](https://cloud.google.com/run)에 해당 이미지를 배포할 수 있습니다.
- [Google Secret Manager](https://cloud.google.com/secret-manager)를 통해 설정된 보안 스트링을 가져올 수 있습니다.

## Prerequisite

이 라이브러리는 아래 프로그램이 실행되는 것을 전제하고 있습니다.

만약 설치되어 있지 않다면, 아래 링크를 토대로 설치해주세요.

- [docker](https://docs.docker.com/engine/install)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install?hl=ko)

## How to install

### poetry

poetry를 사용할 경우 `pyproject.toml`파일에 아래의 depedency를 추가하시면 됩니다.

```yml
[tool.poetry.dependencies]
mlops-utils = {git = "ssh://git@github.com/y9yk/mlops-utils.git", rev = "develop"}
```

### requirements.txt

`requirements.txt`에 아래와 같이 추가한 후 라이브러리를 사용할 수 있습니다.

```bash
mlops-utils @ git+ssh://git@github.com/y9yk/mlops-utils.git@develop
```

## Examples

### Get model from MLflow and pack using BentoML

MLflow에 위치한 모델을 로드하고, BentoML을 이용해서 packing하는 예제는 아래와 같습니다.
- [get_model_from_mlflow_and_pack](./mlops_utils/examples/get_model_from_mlflow_and_pack.md)

### BentoML Build and Containerization

Packing된 모델을 BentoML을 이용해서 빌드, 컨테이너화하는 예제는 아래와 같습니다.
- [bentoml_build_and_containerize](./mlops_utils/examples/bentoml_build_and_containerize.md)

### Docker Tag and Push to GCR

BentoML을 토대로 생성된 이미지를 Google Cloud Registry에 푸시하는 예제는 아래와 같습니다.
- [docker_tag_and_push_to_gcr](./mlops_utils/examples/docker_tag_and_push_to_gcr.md)

### Deploy to Google Cloud Run

BentoML로 생성된 모델 서빙 이미지가 Google Cloud Run에 배포되는 예제는 아래와 같습니다.
- [deploy_to_cloud_run](./mlops_utils/examples/deploy_to_cloud_run.md)

### Get Secret Str using Google Secret Manager

Google Secret Manager를 통해서 관리되는 정보를 가져올 수 있는 예제는 아래와 같습니다.
- [get_secret_str](./mlops_utils/examples/get_secret_str.md)
