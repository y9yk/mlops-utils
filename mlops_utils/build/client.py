import subprocess


# @deprecated
# def run_script(command: str):
#     sh = shell(command)
#     for line in sh.output():
#         print(line)
#     if sh.code != 0:
#         raise Exception(sh.errors)


def run_script(command: str):
    # debug command
    print("-" * 20)
    print(command)
    print("-" * 20)
    # process
    proc = subprocess.Popen(
        command,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
        shell=True,
    )
    while True:
        output = proc.stdout.readline()
        # show progress
        if output:
            print(output.strip().decode("UTF8"))
        # break
        code = proc.poll()
        if code is not None:
            if code == 0:
                break
            else:
                raise Exception(command)


def bentoml_build(model_name: str):
    build_context = f"modules/services/{model_name}"
    config_file_path = f"{build_context}/bentofile.yaml"
    run_script(f"bentoml build -f {config_file_path} {build_context}")


def bentoml_containerize(
    model_name: str,
    model_tag: str,
    git_access_token: str,
):
    run_script(
        f"bentoml containerize {model_name}:{model_tag} \
            --opt build-arg=GIT_ACCESS_TOKEN={git_access_token} \
            --opt progress=plain"
    )


def docker_tag_to_image(
    model_name: str,
    model_tag: str,
    gcp_project: str,
):
    model_image_name = f"gcr.io/{gcp_project}/{model_name}:{model_tag}"
    run_script(f"docker tag {model_name}:{model_tag} {model_image_name}")


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
