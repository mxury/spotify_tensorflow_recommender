from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import pandas as pd
from datetime import datetime
from playlist_artist_graph import Graph


load_dotenv()


def read_public_playlist(spotify_client, owner_id, playlist_id):
    """
    Reads in songs from a public playlist specified by 'playlist_id'. Dumps the resulting songs, their id, and artists
    in a csv file for further reading.
    :param spotify_client: spotipy.Spotify() client
    :param owner_id: id of the owner of the playlist
    :param playlist_id: ID the public playlist
    :return: set of new artists, which become nodes in the search graph
    """
    playlist_data = spotify_client.playlist_items(
        playlist_id,
        fields='items.track.artists.name, items.track.id, items.track.name, items.track.popularity',
    )

    playlist_df = pd.DataFrame()
    # limiting the playlist to 50 tracks to get more playlists
    for track in playlist_data['items'][:50]:
        temp = pd.json_normalize(track)
        # rather brute way to catch bad responses
        if len(temp.columns) != 4:
            continue
        temp['track.artists'] = temp['track.artists'].apply(lambda x: x[0]['name'])
        playlist_df = pd.concat([playlist_df, temp])

    if playlist_df.empty:
        return []

    playlist_df['user_id'] = owner_id
    file_suffix = datetime.now().strftime('%H')
    playlist_df.to_csv(f'./data/user_song_database.csv', mode='a', index=False, header=False)
    return playlist_df['track.artists'].unique().tolist()[:50]


def find_new_playlists(spotify_client, search_term):
    """Finds new playlist given a search term, in this case the search term is an Artists name. Using trackname is too
    specific and doesn't produce any results.
    :param spotify_client:
    :param search_term:
    :return: a tuple of lists(playlist_id, id of playlist owner)
    """
    results = spotify_client.search(q=search_term, type='playlist')
    owners = []
    playlist_ids = []
    for result in results['playlists']['items']:
        owners.append(result['owner']['id'])
        playlist_ids.append(result['id'])

    return playlist_ids, owners


if __name__ == '__main__':
    client_credentials_manager = SpotifyClientCredentials()
    sp_public = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # the id of my personal account
    personal_id = 'kv718oiku8q612q0zi4iaovzb'
    personal_playlist = '0P7Jb1reHqCTbhJ34Lj58s'

    # graph of the playlists and artists the search traverses
    graph = Graph(personal_playlist, personal_id)
    visited = []
    queue = []
    max_depth = 0
    node_id = personal_playlist

    # using a breadth-first search algorithm to scan the song-search graph
    visited.append(node_id)
    queue.append((node_id,1))
    j = 1


    queue = []
    while queue:
        node_id, depth = queue.pop(0)
        max_depth = max(max_depth, depth)
        # print(f'node_id:: {node_id}')

        # the action on a node depends on its type, if the node is a playlist we want to dump all the songs in it in a
        # csv file and then use the artists of those songs to create new nodes in our search graph
        if graph.is_playlist(node_id):
            artists = read_public_playlist(sp_public, graph.playlist_owner[node_id], node_id)
            graph.add_nodes(list(set(artists)), node_id)

        # if the nodes is an artist then we use it to find new playlists
        else:
            playlists, owners = find_new_playlists(sp_public, node_id)
            graph.add_nodes(playlists, node_id)
            # saves looking up the id of the owner of the playlist using a separate API query
            graph.add_playlist_owner(playlists, owners)

        for neighbour in graph[node_id]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append((neighbour, depth+1))

        # brute force of cutting the search, ideally would cut it off after a certain amount of children in the graph
        # TO DO
        j += 1
        if not (j % 1000):
            print(f'j: {j}')
        if j == 10000:
            # pprint.pprint(graph.nodes)
            print(f'max depth: {max_depth}')
            break

