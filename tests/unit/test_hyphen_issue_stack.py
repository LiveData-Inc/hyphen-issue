import aws_cdk as core
import aws_cdk.assertions as assertions

from hyphen_issue.hyphen_issue_stack import HyphenIssueStack

# example tests. To run these tests, uncomment this file along with the example
# resource in hyphen_issue/hyphen_issue_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HyphenIssueStack(app, "hyphen-issue")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
