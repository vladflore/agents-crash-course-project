from typing import Dict, List, Union
from prepare_data import download_repository_data, posts_sections, peek, save_to_file
import weaviate
from load_data import create_collection, load_data
import json

BLOG_POSTS_FILE = "blog.json"

blog_posts = download_repository_data("vladflore", "vladflore.tech.private")

print(f"{len(blog_posts)} posts")

# docs_sections = []
# for doc in repository_data:
#     doc_copy = doc.copy()
#     doc_content = doc_copy.pop("content")
#     chunks = sliding_window(doc_content, 2000, 1000)
#     for doc_section in chunks:
#         doc_section.update(doc_copy)
#     docs_sections.extend(chunks)

sections = posts_sections(blog_posts)

peek(sections)

save_to_file(BLOG_POSTS_FILE, sections)

if sections:
    client: weaviate.WeaviateClient = weaviate.connect_to_local()
    create_collection(client, "Blog")
    with open(BLOG_POSTS_FILE, "r", encoding="utf-8") as f:
        data: List[Dict[str, Union[str, List[str]]]] = json.load(f)
        load_data(client, "Blog", data)
    client.close()
