FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG QRCODR_BUILD_VERSION=0.0.0+docker

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN python -m pip install --no-cache-dir --upgrade pip \
    && printf '%s\n' '"""Build-time version override injected by container build."""' > src/qrcodr/_build_version.py \
    && printf '%s\n' >> src/qrcodr/_build_version.py \
    && printf 'BUILD_VERSION: str | None = "%s"\n' "${QRCODR_BUILD_VERSION}" >> src/qrcodr/_build_version.py \
    && python -m pip install --no-cache-dir .

ENTRYPOINT ["qrcodr", "generate"]
CMD ["--help"]
