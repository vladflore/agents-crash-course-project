import weaviate
from weaviate.classes.generate import GenerativeConfig
import sys

print("Question:", sys.argv[1])

client = weaviate.connect_to_local()

questions = client.collections.use("Blog")

response = questions.generate.near_text(
    query=sys.argv[1],
    # limit=2,
    grouped_task="Write a one long paragraph answer for the question based on the context.",
    generative_provider=GenerativeConfig.ollama(
        api_endpoint="http://host.docker.internal:11434",
        model="llama3.2",
    ),
)

print(response.generative.text)

client.close()
