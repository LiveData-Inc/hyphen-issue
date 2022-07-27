from importlib.metadata import version
from pathlib import Path

import aws_cdk as cdk
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
        # endregion context variables

        # region Lambda
        # region Lambda environment variables
        env_vars = self.get_environ()
        env_vars.update(dict(
            VERSION=__version__,
        ))
        # endregion Lambda environment variables

        # region Function
        with open('lambda-handler.py', encoding='utf8') as fp:
            handler_code = fp.read()

        handler = lambda_.Function(
            self, f'{self.name}Lambda',
            code=lambda_.InlineCode(handler_code),
            handler='index.handler',
            timeout=cdk.Duration.seconds(10),
            runtime=lambda_.Runtime.PYTHON_3_9,
        )
        # endregion Function

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
