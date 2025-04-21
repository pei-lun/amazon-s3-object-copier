ARG PYTHON_VERSION=3.13
ARG DEPLOYMENT_PACKAGE_NAME=amazon_s3_object_copier.zip

FROM public.ecr.aws/lambda/python:${PYTHON_VERSION} AS builder
RUN microdnf install -y binutils findutils && microdnf clean all
COPY requirements.txt /var/task/
RUN pip install -r requirements.txt -t . && \
    rm requirements.txt && \
    find . -type f -name "*.so" -exec strip "{}" \; && \
    find . -regex "^.*\(__pycache__\|\.py[co]\)$" -delete

FROM almalinux:9-minimal
RUN microdnf install -y findutils zip && microdnf clean all
ENV WORK_DIR=/function
WORKDIR ${WORK_DIR}
COPY --from=builder /var/task ${WORK_DIR}/
COPY lambda_function.py ${WORK_DIR}/
ARG DEPLOYMENT_PACKAGE_NAME
ENV DEPLOYMENT_PACKAGE=/tmp/${DEPLOYMENT_PACKAGE_NAME}
CMD test -f ${DEPLOYMENT_PACKAGE} && rm ${DEPLOYMENT_PACKAGE}; \
    find . -regex "^.*\(__pycache__\|\.py[co]\)$" -delete && \
    zip -9r -q ${DEPLOYMENT_PACKAGE} . -x "bin/*"
