import weaviate
import json
import sys

client = weaviate.connect_to_local()

questions = client.collections.use("Blog")

response = questions.query.near_text(query=sys.argv[1], limit=3)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))

client.close()
