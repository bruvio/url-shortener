
FROM python:3.8-slim
MAINTAINER bruvio

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /usr/src/app


COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

COPY ./src/ ./src/
COPY ./tests ./tests
ENTRYPOINT [ "pytest","/usr/src/app/tests" ]
