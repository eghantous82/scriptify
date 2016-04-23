import pprint
import sys

import spotipy
import spotipy.util as util

'''
def show_tracks(results):

    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))
'''


def sync_playlist(playlist_name):

    VALID_RESPONSES = ['Y', 'N', 'y', 'n']
    user_input = ""
    while user_input not in VALID_RESPONSES:
        user_input = input("Would you like to sync " + playlist_name + " (Yy/Nn)? ")

    return user_input


def enumerate_playlists(username):

    scope = 'user-library-modify playlist-read-collaborative playlist-read-private'
    token = util.prompt_for_user_token(username=username,
                                       redirect_uri='http://localhost:8888/callback',
                                       scope=scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id']:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                save_input = sync_playlist(playlist['name'])
                if save_input == 'Y' or save_input == 'y':
                    results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
                    tracks = results['tracks']
                    j = 0
                    track_ids = []
                    for i, item in enumerate(tracks['items']):
                        track = item['track']
                        if j == 50:
                            sp.current_user_saved_tracks_add(track_ids)
                            track_ids.clear()
                            j = 0
                        track_ids.append(track['id'])
                        j += 1
                    sp.current_user_saved_tracks_add(track_ids)
    else:
        print("Can't get token for", username)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        uname = sys.argv[1]
        enumerate_playlists(uname)
    else:
        print("Whoops, need your username!")
        print("usage: python sync_my_tracks [username]")
        sys.exit()
