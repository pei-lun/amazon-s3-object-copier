ARG PYTHON_VERSION=3.13
ARG DEPLOYMENT_PACKAGE_NAME=amazon_s3_object_copier.zip

FROM almalinux:9-minimal
RUN microdnf install -y zip && microdnf clean all
ENV WORK_DIR=/function
WORKDIR ${WORK_DIR}
COPY lambda_function.py ${WORK_DIR}/
ARG DEPLOYMENT_PACKAGE_NAME
ENV DEPLOYMENT_PACKAGE=/tmp/${DEPLOYMENT_PACKAGE_NAME}
CMD ["sh", "-c", "test -f \"${DEPLOYMENT_PACKAGE}\" && rm \"${DEPLOYMENT_PACKAGE}\"; zip -9r -q \"${DEPLOYMENT_PACKAGE}\" . -x \"bin/*\""]
