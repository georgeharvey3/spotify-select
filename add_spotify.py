# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:48:40 2020

@author: George
"""

import os
import spotipy
import spotipy.util as util
from collections import namedtuple
import config
from errors import PlaylistNotFoundException

'''
if os.getcwd() != os.path.dirname(os.path.abspath(__file__)):
    import config
else:
    import Pack.config as config
'''

    
token = util.prompt_for_user_token(username=config.USERNAME, scope=config.SCOPE,
                                   client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET,
                                   redirect_uri=config.REDIRECT_URI)

# create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)

def search_for_album(album_name):
    """Search Spotify for an album
    
    Args:
        album_name (str): Album name to be searched for.

    Returns:
        results (list): List of tuples containing the album artist, album name and album id.
    """

    print(f'Searching for album: {album_name}')

    search_result = spotifyObject.search(q=f'"{album_name}"', limit=20, type='album')

    items = search_result['albums']['items']

    results = []

    for item in items:
        if len(item['artists']) > 1:
            artists = tuple(art['name'] for art in item['artists'])
        else:
            artists = item['artists'][0]['name']

        results.append((artists, item['name'], item['id']))

    return results

def search_for_tracks(album_id):

    """Obtains a list of tracks for a given album_id
    
    Args:
        album_id (str): ID of the album to be searched.

    Returns:
        ids (list): List of track ids that will be added to the playlist.
    """
    
    track_results = spotifyObject.album_tracks(album_id)
    track_results = track_results['items']
    ids = [track['id'] for track in track_results]

    return ids

def add_to_playlist(track_ids, playlist_name):

    """Adds supplied tracks to specified playlist
    
    Args:
        track_ids (list): List of track ids that will be added to the playlist.
    """
    
    playlist_id = find_playlist(playlist_name)
        
    spotifyObject.user_playlist_add_tracks(config.USERNAME, playlist_id,
                                           track_ids, position=None)

def find_playlist(playlist_name):
     
    """Searches a user's playlists for a given name and returns its ID if found

    Args:
        playlist_name (str): Name of the playlist to search for.
    
    Returns:
        playlist_id (str): ID of the playlist.

    Raises:
        PlaylistNotFoundException: If given playlist name cannot be found.
    """

    playlists = spotifyObject.user_playlists(config.USERNAME)

    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']
    
    raise PlaylistNotFoundException("The given playlist name was not found.")
        