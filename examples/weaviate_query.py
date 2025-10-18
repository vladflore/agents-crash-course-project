import weaviate
import json

client = weaviate.connect_to_local()

questions = client.collections.use("Blog")

response = questions.query.near_text(
    query="Is there a mention of some renound american university where AI is being thought?",
    limit=2
)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))

client.close()
