
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = os.environ["GITHUB_REPOSITORY"]
TOKEN = os.environ["GITHUB_TOKEN"]
JSON_FILE = Path("wallpaper.json")


def get_image_path(url):
    parsed = urllib.parse.urlparse(url)
    parts = urllib.parse.unquote(
        parsed.path
    ).strip("/").split("/")

    if parsed.netloc == "raw.githubusercontent.com":
        if len(parts) >= 6 and parts[2:4] == [
            "refs", "heads"
        ]:
            return "/".join(parts[5:])
        if len(parts) >= 4:
            return "/".join(parts[3:])

    if parsed.netloc == "github.com":
        if len(parts) >= 5 and parts[2] == "blob":
            return "/".join(parts[4:])

    return None


def get_last_update(url):
    path = get_image_path(url)

    if not path:
        return datetime.min.replace(tzinfo=timezone.utc)

    query = urllib.parse.urlencode({
        "path": path,
        "per_page": 1
    })

    api_url = (
        f"https://api.github.com/repos/{REPO}/commits?"
        f"{query}"
    )

    request = urllib.request.Request(
        api_url,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )

    try:
        with urllib.request.urlopen(request) as response:
            commits = json.load(response)

        if not commits:
            return datetime.min.replace(
                tzinfo=timezone.utc
            )

        date = commits[0]["commit"]["committer"]["date"]
        return datetime.fromisoformat(
            date.replace("Z", "+00:00")
        )

    except Exception as error:
        raise RuntimeError(
            f"Gagal mengambil tanggal file {path}: {error}"
        )


with JSON_FILE.open("r", encoding="utf-8") as file:
    wallpapers = json.load(file)

wallpapers.sort(
    key=lambda item: int(item.get("id",0)),
    reverse=True
)

with JSON_FILE.open("w", encoding="utf-8") as file:
    json.dump(
        wallpapers,
        file,
        indent=2,
        ensure_ascii=False
    )
    file.write("\n")

print("Wallpaper berhasil diurutkan!")
