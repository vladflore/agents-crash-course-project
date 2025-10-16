import weaviate
import sys


if len(sys.argv) < 2:
    raise Exception("Provide the name of the collection")

client = weaviate.connect_to_local()

collection_name = sys.argv[1]

print(f"Is client ready? {client.is_ready()}")

try:
    collection = client.collections.get(collection_name)
    print(f"Collection {collection_name} exists.")
except Exception as e:
    print(f"Collection {collection_name} does not exist.")
    print(e)

client.close()
