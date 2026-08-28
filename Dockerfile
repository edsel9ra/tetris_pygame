FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        libasound2 \
        libfontconfig1 \
        libfreetype6 \
        libglib2.0-0 \
        libsm6 \
        libsdl2-2.0-0 \
        libsdl2-image-2.0-0 \
        libsdl2-mixer-2.0-0 \
        libsdl2-ttf-2.0-0 \
        libx11-6 \
        libxext6 \
        libxi6 \
        libxinerama1 \
        libxrandr2 \
        libxrender1 \
        libxcursor1 \
        libxxf86vm1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --requirement requirements.txt

COPY tetris.py .

CMD ["python", "tetris.py"]
