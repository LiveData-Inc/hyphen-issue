# NOTE: expects the ${LAMBDA_TASK_ROOT} environment variable to be /var/task in both base images

ARG BUILD_IMG
ARG DEPLOY_IMG

# layer 1: build image
FROM $BUILD_IMG as package-image

WORKDIR ${LAMBDA_TASK_ROOT}

# NOTE: we don't need .pyc files in this layer, since a later layer handles that
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

ARG PIP_INDEX_URL
ARG PIP_TRUSTED_HOST

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -t .
RUN rm requirements.txt


# layer 2: deploy image
FROM $DEPLOY_IMG

# copy in any unzipped Lambda layers and our own extensions, if any
COPY layers/ /opt/
RUN rm -f /opt/.gitignore

# this lets extensions use the handler's site-packages
ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

# NOTE: src refers back to package-image layer directory tree, and so needs to be explicit; 
#       "." in the src arg of COPY refers to the current directory of the build host, which is not what we want here.
COPY --from=package-image ${LAMBDA_TASK_ROOT} .
COPY lambda_handler.py .

# copy in any local files and/or folders from docker_src/packages
COPY packages .
RUN rm -f .gitignore

# compile .py to .pyc
RUN python -m compileall .

CMD [ "lambda_handler.handler" ]
