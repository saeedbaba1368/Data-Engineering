import subprocess
import json
import logging

logging.basicConfig(filename="logs.log", encoding="utf-8", level=logging.DEBUG)


def main(titles,subpath):

    for title, url in titles.items():
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "--no-check-certificate",
                    "--skip-download",
                    "--write-subs",
                    f'-o "transcripts/{subpath}/{"_".join(title.split())}.%(ext)s"',
                    f"{url}",
                ],
                shell=True,
            )
        except Exception as e:
            logging.error(f"Could not run subprocess on -> {title}:{url}")
            continue


if __name__ == "__main__":
    title_names_file = "data/philosophy_engineered_titles.json"
    with open(title_names_file) as f:
        data = json.load(f)

    main(titles=data, subpath = "philosophy_engineered")
