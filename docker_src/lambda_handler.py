import logging
import os

from aws_utils import ExceptionHandlers, setup_root_logger, standard_lambda_handler

# region logger setup
setup_root_logger(config_dict=dict(
    version=1,
    incremental=True,
    loggers={
        "hyphen-issue": {
            "level": "DEBUG"
        },
    }
))
logger = logging.getLogger('hyphen-issue')
# endregion


def handle_event(event: dict, context: object) -> dict:
    logger.debug(f'{event=} {context=}')
    logger.debug(f'{os.environ=}')

    rv = dict(
        statusCode=200,
        body=dict(
            log_stream_name=context.log_stream_name,
            request_id=context.aws_request_id
        )
    )

    return rv


@standard_lambda_handler(logger=logger, exception_handler=ExceptionHandlers.SUCCESS)
def handler(event: dict, context: object) -> dict:
    return handle_event(event, context)
