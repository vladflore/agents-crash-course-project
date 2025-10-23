import weaviate

# import json
from weaviate.classes.config import Configure
from typing import Any, Dict, List, Union
from weaviate.classes.config import Configure, DataType, Property
import tqdm


def create_collection(client: weaviate.WeaviateClient, collection_name: str) -> None:
    collection_exists: bool = client.collections.exists(collection_name)
    if collection_exists:
        print(f"{collection_name} exists and will be deleted.")
        client.collections.delete(collection_name)
        collections: List[str] = client.collections.list_all()
        if collection_name not in collections:
            print(f"{collection_name} successfully deleted.")

    print(f"Creating {collection_name} ...")

    _ = client.collections.create(
        name=collection_name,
        properties=[
            Property(name="title", data_type=DataType.TEXT),
            Property(name="section", data_type=DataType.TEXT),
            Property(name="header_hierarchy", data_type=DataType.TEXT),
        ],
        vector_config=Configure.Vectors.text2vec_ollama(
            api_endpoint="http://host.docker.internal:11434",
            model="embeddinggemma",
        ),
        generative_config=Configure.Generative.ollama(
            api_endpoint="http://host.docker.internal:11434",
            model="llama3.2",
        ),
    )

    collections = client.collections.list_all()
    if collection_name in collections:
        print(f"{collection_name} created successfully.")


def load_data(
    client: weaviate.WeaviateClient,
    collection_name: str,
    data: List[Dict[str, Union[str, List[str]]]],
) -> None:
    collection = client.collections.use(collection_name)
    with collection.batch.fixed_size(batch_size=5) as batch:
        for count, blog_post_section in tqdm.tqdm(enumerate(data)):
            title: str = blog_post_section.get("title", "No Title")
            # date: str = blog_post_section.get("date", "No Date")
            tags: List[str] = blog_post_section.get("tags", [])
            # filename: str = blog_post_section.get("filename", "No Filename")
            section: str = blog_post_section.get("content", "No Content")
            # index: int = blog_post_section.get("index", 0)
            header_hierarchy: Dict[str, str] = blog_post_section.get(
                "header_hierarchy", {}
            )
            batch.add_object(
                {
                    "title": title,
                    # "date": date,
                    # "tags": tags,
                    # "filename": filename,
                    "section": section,
                    # "index": index,
                    "header_hierarchy": " > ".join(
                        f"{header_level}: {header_text}"
                        for header_level, header_text in header_hierarchy.items()
                    ),
                }
            )

            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break

    failed_objects: List[Any] = collection.batch.failed_objects
    if failed_objects:
        print(f"Number of failed imports: {len(failed_objects)}")
        print(f"First failed object: {failed_objects[0].message}")

    response = collection.aggregate.over_all(total_count=True)
    print(response.total_count)
