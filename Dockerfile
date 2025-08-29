# ===============================
# Base image with Python
# ===============================
FROM python:3.11-slim AS base

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Build whisper.cpp binary
# ===============================
FROM base AS whispercpp

RUN git clone https://github.com/ggerganov/whisper.cpp.git /whisper && \
    make -C /whisper

# ===============================
# Final runtime image
# ===============================
FROM base

# Copy whisper.cpp binary + models
COPY --from=whispercpp /whisper/main /app/whisper/main
COPY --from=whispercpp /whisper/models /app/whisper/models

# Copy app code
COPY . .

# Environment variables for runtime selection
# Options: whisper_cpp | openai | whisper_lib
ENV TRANSCRIBE_BACKEND=whisper_cpp
ENV WHISPER_CPP_BIN=/app/whisper/main
ENV WHISPER_CPP_MODEL=/app/whisper/models/ggml-base.en.bin
ENV OPENAI_API_KEY=""
ENV WHISPER_MODEL=base

# Expose port (if running API server)
EXPOSE 8000

CMD ["python", "main.py"]
