import io
import zipfile
import requests
import frontmatter
import os

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


vladflore_dot_tech = read_repo_data("vladflore", "vladflore.tech.private")

print(len(vladflore_dot_tech))

for md in vladflore_dot_tech[:5]:
    print(md["filename"])
    # print(md["content"])
