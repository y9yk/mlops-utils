from mlflow.tracking import MlflowClient


def yield_artifacts(run_id, path=None):
    """Yield all artifacts in the specified run"""
    client = MlflowClient()
    for item in client.list_artifacts(run_id, path):
        if item.is_dir:
            yield from yield_artifacts(run_id, item.path)
        else:
            yield item.path


def fetch_logged_data(run_id):
    """Fetch params, metrics, tags, and artifacts in the specified run"""
    client = MlflowClient()
    data = client.get_run(run_id).data
    # Exclude system tags: https://www.mlflow.org/docs/latest/tracking.html#system-tags
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = list(yield_artifacts(run_id))
    return {
        "params": data.params,
        "metrics": data.metrics,
        "tags": tags,
        "artifacts": artifacts,
    }


def fetch_run_id(model_name, model_stage=None):
    """Fetch run_id in the specified model_name on model_stage"""
    # get model from mlflow
    client = MlflowClient()

    # NOTE: return latest_versions per stage
    latest_versions = client.get_latest_versions(name=model_name, stages=model_stage)
    assert (
        latest_versions and len(latest_versions) > 0
    ), f"There is not latest version of {model_name} on {model_stage}"

    #
    return latest_versions[0].run_id


def fetch_logged_info(model_name, model_stage=None):
    """Fetch run_id in the specified model_name on model_stage"""
    # get model from mlflow
    client = MlflowClient()

    # NOTE: return latest_versions per stage
    latest_versions = client.get_latest_versions(name=model_name, stages=model_stage)
    assert (
        latest_versions and len(latest_versions) > 0
    ), f"There is not latest version of {model_name} on {model_stage}"

    #
    if model_stage:
        data = latest_versions.get(model_stage)[0]
    else:
        # NOTE: 에러 발생할 가능성이 있다. -> stage별로 모델 저장된 후, 테스트 필요
        data = latest_versions[0]
    return {
        "run_id": data.run_id,
        "model_name": data.name,
        "artifact_uri": data.source,
        "status": data.status,
    }


def fetch_logged_full_info(run_id: str):
    """Fetch model information in the specified run"""
    client = MlflowClient()
    data = client.get_run(run_id).info
    return {
        "run_id": data.run_id,
        "run_uuid": data.run_uuid,
        "run_name": data.run_name,
        "artifact_uri": os.path.join(data.artifact_uri, "model"),
        "lifecycle_stage": data.lifecycle_stage,
        "experiment_id": data.experiment_id,
        "end_time": data.end_time,
        "status": data.status,
        "user_id": data.user_id,
    }
