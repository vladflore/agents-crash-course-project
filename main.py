import io
import zipfile
import requests
import frontmatter
import os
import re

GH_TOKEN = os.getenv("GH_TOKEN")


def read_repo_data(owner: str, name: str) -> list[dict[str, object]]:
    url = f"https://api.github.com/repos/{owner}/{name}/zipball/main"
    headers = {"Authorization": f"Bearer {GH_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download repository: {response.status_code} - {response.text}"
        )

    repository_data = []

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        for file_info in zf.infolist():
            filename = file_info.filename.lower()

            if "/content/posts/" not in filename:
                continue

            if not filename.endswith(".md") and not filename.endswith(".mdx"):
                continue

            try:
                with zf.open(file_info) as f_in:
                    content = f_in.read().decode("utf-8", errors="ignore")
                    post = frontmatter.loads(content)
                    data = post.to_dict()
                    data["filename"] = filename
                    repository_data.append(data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

    return repository_data


vladflore_dot_tech_docs = read_repo_data("vladflore", "vladflore.tech.private")

print(len(vladflore_dot_tech_docs))

for md in vladflore_dot_tech_docs:
    print(md["filename"])
    # print(md["content"])

# print(vladflore_dot_tech_docs[1])


def sliding_window(seq, size, step):
    """
    i.e. overlapping chunking
    """
    if size < 0 or step < 0:
        raise ValueError("size and step must be positive")
    result = []
    n = len(seq)
    for i in range(0, n, step):
        chunk = seq[i : i + size]
        result.append({"start": i, "chunk": chunk})
        if i + size >= n:
            break
    return result


docs_sections = []
for doc in vladflore_dot_tech_docs:
    doc_copy = doc.copy()
    doc_content = doc_copy.pop("content")
    chunks = sliding_window(doc_content, 2000, 1000)
    for doc_section in chunks:
        doc_section.update(doc_copy)
    docs_sections.extend(chunks)

# print(len(docs_sections))

# for doc_section in docs_sections[:10]:
#     print(f"{doc_section['start']} - {doc_section['filename']}")
#     print(doc_section['chunk'])


def split_markdown_by_level(text, level=2):
    header_pattern = r"^(#{" + str(level) + r"} )(.+)$"
    pattern = re.compile(header_pattern, re.MULTILINE)

    parts = pattern.split(text)

    sections = []
    for i in range(1, len(parts), 3):
        header = parts[i] + parts[i + 1]
        header = header.strip()

        content = ""
        if i + 2 < len(parts):
            content = parts[i + 2].strip()

        if content:
            section = f"{header}\n\n{content}"
        else:
            section = header
        sections.append(section)

    return sections


docs_sections = []
for doc in vladflore_dot_tech_docs:
    doc_copy = doc.copy()
    doc_content = doc_copy.pop("content")
    sections = split_markdown_by_level(doc_content, level=2)
    for section in sections:
        doc_section = doc_copy.copy()
        doc_section["section"] = section
        docs_sections.append(doc_section)

print(len(docs_sections))

for doc_section in docs_sections[:3]:
    print(f"{doc_section['title']}")
    print(f"{doc_section['filename']}")
    print(f"{doc_section['section'][:100]}")

# print(docs_sections[0].keys())
