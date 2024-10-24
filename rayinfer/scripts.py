import logging
import os

import ray
from ray import serve
from ray.serve.exceptions import RayServeException
from vllm.entrypoints.openai.cli_args import make_arg_parser
from vllm.utils import FlexibleArgumentParser

from rayinfer.ray_server import build_app


logger = logging.getLogger("launch_rayinfer")


def parse_args():
    # arg_parser = FlexibleArgumentParser()
    parser = FlexibleArgumentParser()

    # parser = make_arg_parser(arg_parser)
    subparsers = parser.add_subparsers(required=True, dest="subparser")
    serve_parser = subparsers.add_parser(
        "vllm",
        help="Start the vLLM OpenAI Compatible API server",
        usage="rayinfer vllm <model> [options]",
    )
    serve_parser.add_argument("model", type=str, help="The model tag to serve")
    serve_parser = make_arg_parser(serve_parser)

    args = parser.parse_args()

    return args


def main():
    # parse arguments
    args = parse_args()
    print(f"Arguments: {vars(args)}")

    # connect to Ray
    ray.init()
    print(f"Resources: {ray.cluster_resources()}")

    # get ray env variables
    ray_restart = bool(int(os.getenv("RAY_RESTART_JOB", "0")))
    ray_job_name = os.getenv("RAY_JOB_NAME", "vllm")
    ray_route_prefix = os.getenv("RAY_ROUTE_PREFIX", "/")
    ray_blocking = bool(int(os.getenv("RAY_BLOCKING", "0")))

    # (optional) delete existing app
    if ray_restart:
        try:
            handle = serve.get_app_handle(name=ray_job_name)
            serve.delete(name=ray_job_name)
        except RayServeException:
            logger.info("Application not found, nothing to delete")

    # launch apps
    app = build_app(args)
    handle = serve.run(
        app,
        blocking=ray_blocking,
        name=ray_job_name,
        route_prefix=ray_route_prefix,
    )
