from shell import shell


def run_script(command: str):
    sh = shell(command)
    errors = sh.errors()
    try:
        assert len(errors) == 0
        return sh.output()
    except:
        raise Exception(errors)


def get_gcp_project():
    command = "gcloud config get-value project"
    return run_script(command)


def bentoml_build(model_name: str):
    build_context = f"modules/services/{model_name}"
    config_file_path = f"{build_context}/bentofile.yaml"
    run_script(f"bentoml build -f {config_file_path} {build_context}")


def bentoml_containerize(
    model_name: str,
    git_access_token: str,
):
    run_script(
        f"bentoml containerize {model_name} \
            --opt build-arg=GIT_ACCESS_TOKEN={git_access_token} \
            --opt progress=auto"
    )


def docker_tag_to_image(
    model_name: str,
    model_tag: str,
    gcp_project: str,
):
    model_image_name = f"gcr.io/{gcp_project}/{model_name}:{model_tag}"
    run_script(f"docker tag {model_name} {model_image_name}")


def docker_push_to_gcr(
    model_name: str,
    model_tag: str,
    gcp_project: str,
):
    # gcloud auth configure-docker
    model_image_name = f"gcr.io/{gcp_project}/{model_name}:{model_tag}"
    run_script(f"docker push {model_image_name}")


def deploy_to_cloud_run(
    model_name: str,
    model_tag: str,
    gcp_project: str,
    gcp_region: str,
    gcp_service_port: int,
    gcp_service_cpu_amount: int = 1,
    gcp_service_mem_amount: str = "512Mi",
    gcp_service_min_instances: int = 0,
    gcp_service_max_instances: int = 100,
    gcp_service_concurrency: int = 80,
    gcp_service_timeout: int = 300,
):
    model_image_name = f"gcr.io/{gcp_project}/{model_name}:{model_tag}"
    command = f"gcloud run deploy {gcp_project} \
                --image {model_image_name} \
                --region {gcp_region} \
                --port {gcp_service_port} \
                --allow-unauthenticated \
                --no-cpu-throttling \
                --cpu {gcp_service_cpu_amount} \
                --memory {gcp_service_mem_amount} \
                --min-instances {gcp_service_min_instances} \
                --max-instances {gcp_service_max_instances} \
                --execution-environment gen1 \
                --concurrency {gcp_service_concurrency} \
                --timeout {gcp_service_timeout}"
    run_script(command)
