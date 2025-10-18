import io
import zipfile
import requests
import frontmatter
import os
import re
from collections import defaultdict
import json
from typing import Any, Dict, List

GH_TOKEN = os.getenv("GH_TOKEN")


def download_repository_data(
    repository_owner: str, repository_name: str
) -> List[Dict[str, Any]]:
    repository_url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/zipball/main"

    headers = {"Authorization": f"Bearer {GH_TOKEN}"}
    response = requests.get(repository_url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"Failed to download repository: {response.status_code} - {response.text}"
        )

    repository_data: List[Dict[str, Any]] = []

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
                    del data["images"]
                    data["filename"] = os.path.basename(filename)
                    repository_data.append(data)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

    return repository_data


def sliding_window(seq: str, size: int, step: int) -> List[Dict[str, Any]]:
    """
    i.e. overlapping chunking
    """
    if size < 0 or step < 0:
        raise ValueError("size and step must be positive")
    result: List[Dict[str, Any]] = []
    n = len(seq)
    for i in range(0, n, step):
        chunk = seq[i : i + size]
        result.append({"start": i, "chunk": chunk})
        if i + size >= n:
            break
    return result


def split_markdown_by_level(text: str, level: int = 2) -> List[str]:
    header_pattern = r"^(#{" + str(level) + r"} )(.+)$"
    pattern = re.compile(header_pattern, re.MULTILINE)

    parts = pattern.split(text)

    sections: List[str] = []
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


def posts_sections(blog_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    docs_sections: List[Dict[str, Any]] = []
    for doc in blog_posts:
        doc_copy = doc.copy()
        doc_content = doc_copy.pop("content")
        sections = split_markdown_by_level(doc_content, level=2)
        for section in sections:
            doc_section = doc_copy.copy()
            doc_section["section"] = section
            docs_sections.append(doc_section)
    return docs_sections


def peek(sections: List[Dict[str, Any]]) -> None:
    print(f"{len(sections)} sections")
    for section in sections[:7]:
        print(json.dumps(section, default=str, indent=2))

    title_counts: defaultdict[str, int] = defaultdict(int)
    for section in sections:
        title_counts[section["title"]] += 1

    for title, count in title_counts.items():
        print(f"{title}: {count} sections")

    assert len(sections) == sum(title_counts.values())


def save_to_file(filename: str, sections: List[Dict[str, Any]]) -> None:
    with open(filename, "w", encoding="utf-8") as f_out:
        json.dump(sections, f_out, indent=2, default=str)
