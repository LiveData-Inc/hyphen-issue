#!/usr/bin/env python3
from aws_cdk import App, Environment
from cdk_utils import register_utils

from hyphen_issue.hyphen_issue_stack import HyphenIssueStack

app = App()
register_utils(app)

HyphenIssueStack(
    app, f'{HyphenIssueStack.name}-{app.get_context("env")}',
    env=Environment(account=app.get_context('account'), region=app.get_context('region')),
)

app.synth()
