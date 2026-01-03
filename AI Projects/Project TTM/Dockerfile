FROM python:3.11

WORKDIR /app

# LiveKit's rtc module loads native libraries; slim images omit some runtime deps.
# libgobject-2.0.so.0 is provided by libglib2.0-0 on Debian.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libstdc++6 \
    libasound2 \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
CMD ["start"]