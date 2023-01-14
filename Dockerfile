FROM python:3

VOLUME [ "/usr/local/src/data" ]
WORKDIR "/usr/local/src"

ENV SAMPLE_TIME="300"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY "./src" "."

ENTRYPOINT [ "python", "./main.py" ]
