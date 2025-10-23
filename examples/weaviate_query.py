import weaviate
import json
import sys
from weaviate.collections.classes.grpc import MetadataQuery


client = weaviate.connect_to_local()

questions = client.collections.use("Blog")

response = questions.query.near_text(
    query=sys.argv[1],
    limit=10,
    return_metadata=MetadataQuery(distance=True),
)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))
    print(f"Distance to query: {obj.metadata.distance:.3f}")

client.close()
