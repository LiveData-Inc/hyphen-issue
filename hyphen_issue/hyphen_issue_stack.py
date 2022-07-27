from importlib.metadata import version
from pathlib import Path

import aws_cdk as cdk
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_lambda as lambda_
from cdk_utils import StackMixin
from constructs import Construct

__version__ = version(__package__)
print(f'{__package__} {__version__=}')


class HyphenIssueStack(StackMixin, cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # region context variables
        env = self.ensure_context('env')
        arch = self.ensure_context('arch')
        # endregion context variables

        # region Lambda
        # region Lambda environment variables
        env_vars = self.get_environ()
        env_vars.update(dict(
            VERSION=__version__,
        ))
        # endregion Lambda environment variables

        # region DockerImageCode
        docker_folder = Path('docker_src')
        self.setup_docker_folder(docker_folder)

        build_args = self.get_docker_build_args(arch=arch)

        docker_image = lambda_.DockerImageCode.from_image_asset(
            directory=str(docker_folder),
            build_args=build_args,
            invalidation=ecr_assets.DockerImageAssetInvalidationOptions(
                build_args=False
            ),
            extra_hash=__version__ + arch,
        )
        # endregion DockerImageCode

        # region DockerImageFunction
        handler = lambda_.DockerImageFunction(
            self, f'{self.name}Lambda',
            function_name=f'{self.name}Lambda-{env}',
            description='testing pythonic config extension',
            current_version_options=lambda_.VersionOptions(
                description=__version__,
            ),
            code=docker_image,
            memory_size=256,
            timeout=cdk.Duration.seconds(10),
            environment=env_vars,
            architecture=lambda_.Architecture.ARM_64 if arch == 'ARM_64' else lambda_.Architecture.X86_64,
        )
        # endregion DockerImageFunction

        # region alias
        alias = handler.add_alias(
            alias_name=env,
            description=__version__,
            provisioned_concurrent_executions=0,
            retry_attempts=0,
        )
        # endregion alias

        # region function URL
        fn_url = alias.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE
        )
        # endregion function URL
        # endregion Lambda

        # region outputs
        cdk.CfnOutput(self, "FunctionUrl", value=fn_url.url)
        # endregion outputs
