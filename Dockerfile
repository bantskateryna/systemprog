FROM python:3.11-slim

WORKDIR /app

COPY head.py uniq.py ./  
COPY test/ ./test/

RUN pip install pytest

ENTRYPOINT ["bash"]
