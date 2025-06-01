# Knowledge Base App

Simple knowledge base app that act as source for RAG.

## Technology Stack
- **Python 3.13**
- **FastAPI**

## Run using Docker
- Build the Docker image:
```sh
docker build -t cli-sageknowledge-base .
```
- Run the Docker container:
```sh
docker run -d -p 4000:4000 lowe-cli-knowledge-base
```
- Access the app at `http://localhost:4000`

## Run using uv
- Install the `uv` package manager: https://docs.astral.sh/uv/getting-started/installation/
- Install the package using `uv`:
```sh
uv sync
```
- Run the app:
```sh
uv run fastapi dev --port 4000
```