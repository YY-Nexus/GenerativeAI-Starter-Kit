FROM python:3.11-slim

LABEL maintainer="YY-Nexus <contact@yynexus.com>"
LABEL description="GenerativeAI-Starter-Kit Docker Image"

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install .

EXPOSE 8000

CMD ["uvicorn", "RAG.examples.basic_rag.langchain.api_sync:app", "--host", "0.0.0.0", "--port", "8000"]
