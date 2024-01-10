import json
import re


def main():
    with open("data/video_metadata.txt", "r") as metadata:
        data = metadata.read().splitlines()

    output = {}
    pointer = 0
    while pointer <= len(data) - 1:
        current_line = data[pointer]
        if "[youtube] Extracting URL:" in current_line:
            video_name = ""
            counter = 0
            for i in range(pointer, len(data)):
                info_line = data[i]
                if "[info]" in info_line:
                    video_name = data[i + 1]
                    break
                counter += 1
            pointer = pointer + counter
            if video_name:
                results = [
                    (m.start(0), m.end(0))
                    for m in re.finditer(r"\[(.*?)\]", video_name)
                ]
                if not results:
                    continue

                idxs = results[-1] if len(results) == 2 else results[-2]
                start = "Destination:"
                idx1 = video_name.index(start)
                idx2 = idxs[0]
                res = ""
                for idx in range(idx1 + len(start) + 1, idx2):
                    res = res + video_name[idx]
                output[res.strip()] = current_line.split("URL:")[-1].strip()
        else:
            pointer += 1

    return output


if __name__ == "__main__":
    results = main()
    with open("data/titles.json", "w") as f:
        json.dump(results, f)
