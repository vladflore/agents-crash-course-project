https://docs.weaviate.io/weaviate/quickstart/local?__hstc=13542376.f55c3263c35488f5a731b4face5f3953.1756585221955.1758908448861.1758919894544.8&__hssc=13542376.1.1758919894544&__hsfp=2903186342

```shell
ollama pull nomic-embed-text
ollama pull llama3.2

docker compose up -d
docker compose down

uv add weaviate-client
```

```shell
docker compose exec -ti weaviate sh -c "wget --header=\"Content-Type: application/x-www-form-urlencoded\" --post-data=\$'{\\n  \"model\": \"llama3.2:latest\",\\n  \"prompt\": \"Why is the sky blue?\"\\n}' --output-document - http://host.docker.internal:11434/api/generate"
```

http://localhost:8080/v1/schema/Blog

```shell
curl -X POST http://127.0.0.1:11434/api/embed -d '{"model": "nomic-embed-text", "input": "test"}'
curl -X POST http://127.0.0.1:11434/api/embed -d '{"model": "mxbai-embed-large", "input": "test"}'
```
