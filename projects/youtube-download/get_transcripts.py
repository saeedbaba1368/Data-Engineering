import subprocess
import pathlib
import json
import logging

logging.basicConfig(filename="logs.log", encoding="utf-8", level=logging.DEBUG)


def main(titles):

    for title, url in titles.items():
        try:
            subprocess.run(
                [
                    "yt-dlp",
                    "--no-check-certificate",
                    "--skip-download",
                    "--write-subs",
                    f'-o "transcripts/{"_".join(title.split())}.%(ext)s"',
                    f"{url}",
                ],
                shell=True,
            )
        except Exception as e:
            logging.error(f"Could not run subprocess on -> {title}:{url}")
            continue


if __name__ == "__main__":
    with open("data/titles.json") as f:
        data = json.load(f)

    main(titles=data)
