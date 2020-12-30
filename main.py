import add_spotify
import pyperclip
import config
import time
import os

album_name = pyperclip.paste()
5
if album_name is None:
    print('You must copy the album name to the clipboard first')

results = add_spotify.search_for_album(album_name)

if len(results) == 0:
    print(f'Album: {album_name} not found.')
    time.sleep(2)
elif len(results) > 1:
    for i, details in enumerate(results):
        print(f'{i+1}: {details[1]} by {details[0]}')
    num = input("Select the album you'd like to add: ")
    selection = results[int(num)-1]
    print(f"Adding '{selection[1]}' by '{selection[0]}' to {config.PLAYLIST_NAME}")
    ids = add_spotify.search_for_tracks(selection[2])
    add_spotify.add_to_playlist(ids, config.PLAYLIST_NAME)
    time.sleep(1)
else:
    print(f"Adding '{results[0][1]}' by '{results[0][0]}' to {config.PLAYLIST_NAME}")
    ids = add_spotify.search_for_tracks(results[0][2])
    add_spotify.add_to_playlist(ids, config.PLAYLIST_NAME)
    time.sleep(1)

