# Get Videos and Parse Transcripts

- Cheatsheet: https://cheat.sh/yt-dlp

## How to Run

1. Download the videos and metadata with. Move metadata to data/
```shell
yt-dlp -o "videos/{your_subdir_name}/%(title)s.%(ext)s"  {youtube_channel_name} > {your_subdir_name}_metadata.txt
```
example
```shell
yt-dlp -o "videos/TheoreticalBullshit/%(title)s.%(ext)s"  https://www.youtube.com/@TheoreticalBullshit > TheoreticalBullshit_metadata.txt
```
2. Run
```shell
python parse_metadata.py
```
update variables
```python
pathtofile = ""
titles_path = ""
```
3. Run
```shell
python get_transcripts.py
```
you will probably get a new output folder, i dont know how to get yt-dlp to write to existing folder
4. Run
```shell
python parse_transcripts.py
```

## For downloading audio only

1. First install ffmpeg (for windows)

```shell
choco install ffmpeg
```

2.  Run specifing the "get_audio" function
``` shell
python get_transcripts.py
```

NOTE: I DO NOT CARE TO MAKE THIS A COMMAND LINE TOOL

## Resources

### Alternative youtube libraries

- https://github.com/yt-dlp/yt-dlp
- https://github.com/ytdl-org/youtube-dl
- https://github.com/Tyrrrz/YoutubeDownloader
- https://github.com/Bluegrams/Vividl
- https://github.com/jely2002/youtube-dl-gui
- https://github.com/shaked6540/YoutubePlaylistDownloader
- https://github.com/pytube/pytube
- https://github.com/Athlon1600/youtube-downloader
- https://github.com/aandrew-me/ytDownloader
- https://github.com/Tzahi12345/YoutubeDL-Material

### Alternative translation libraries

- https://github.com/nidhaloff/deep-translator
- https://github.com/terryyin/translate-python
- https://github.com/argosopentech/argos-translate
- https://github.com/JohnSnowLabs/nlu
- https://github.com/UlionTse/translators
- https://github.com/ssut/py-googletrans
- https://github.com/Saravananslb/py-googletranslation