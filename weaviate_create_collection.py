import weaviate
from weaviate.classes.config import Configure

client = weaviate.connect_to_local()

collection_name = "Question"

collection_exists = client.collections.exists(collection_name)
if collection_exists:
    print(f"{collection_name} exists and will be deleted.")
    client.collections.delete(collection_name)
    collections = client.collections.list_all()
    if collection_name not in collections:
        print(f"{collection_name} successfully deleted.")

print(f"Creating {collection_name} ...")

questions = client.collections.create(
    name=collection_name,
    vector_config=Configure.Vectors.text2vec_ollama(
        api_endpoint="http://host.docker.internal:11434",
        model="nomic-embed-text",
    ),
    generative_config=Configure.Generative.ollama(
        api_endpoint="http://host.docker.internal:11434",
        model="llama3.2",
    ),
)

collections = client.collections.list_all()
if collection_name in collections:
    print(f"{collection_name} created successfully.")

client.close()  # Free up resources
