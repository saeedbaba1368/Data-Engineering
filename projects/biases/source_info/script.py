import youtube_dl
import pickle


def get(PLAYLIST_ID):
	'''
	Visit the Channel page and view page source
	Search for externalID and copy the value into PLAYLIST_ID below
	Change the C to a U so it begins UU instead of UC (U=Upload Playlist)
	'''
	with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
		playd = ydl.extract_info(PLAYLIST_ID, download=False)

	with open('playlist.pickle', 'wb') as f:
		pickle.dump(playd, f, pickle.HIGHEST_PROTOCOL)

	with open('playlist.pickle', 'rb') as f:
		data = pickle.load(f)

		for video in data['entries']:
			for property in ['title']:
				print(video.get(property))



"""
Getting the metadata:

1) pip install youtube-dl

2) run in CMD: youtube-dl --get-id https://www.youtube.com/playlist?list={playlist id}  > {file_name}.txt

3) run in CMD: for /R %f in (*.txt) do type “%f” >> c:{path_to_directory}\{file_name}.txt

4) run the script below

"""

import re

pattern = re.compile(r"(?<=What is )[^[]*")

with open("search_data.txt", "w") as outfile:
	with open("combined.txt","r") as infile:
		for line in infile:
			matches = re.findall(pattern,line)
			if matches:
				for match in matches:
					outfile.write(match.strip()+"\n")