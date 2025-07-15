FROM python:3.11.5-slim

RUN pip install --no-cache-dir uv==0.6.4 && python -m uv venv

ENV PATH="/.venv/bin:$PATH"
ENV LOGGER_CONFIG_FILE="conf/logging.conf"
ENV LOGGER_NAME="datadog"

RUN apt-get update
RUN apt-get install gcc libc6-dev -y --no-install-recommends
RUN apt-get autoremove -yqq --purge
RUN rm -rf /var/cache/apt
RUN apt-get clean

WORKDIR /build
COPY pyproject.toml uv.lock .
COPY src src
RUN uv build --no-cache --verbose
RUN uv pip install ./dist/*.whl

WORKDIR /app
RUN rm -rf /build
COPY ./conf/ ./conf/
COPY start.sh .

RUN chmod +x start.sh

CMD ["/bin/sh", "./start.sh"]