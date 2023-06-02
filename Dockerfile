FROM python:3.8.13-slim

EXPOSE 8503

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/apt \
    apt-get update -y && apt-get upgrade -y

RUN --mount=type=cache,target=/root/.cache/apt \
    apt-get install -y build-essential procps nano git docker.io


# Install dependencies:
COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY .  /app

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
