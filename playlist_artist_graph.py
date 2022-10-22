class Graph:
    """
    A class that creates a graph connection between playlists and artists
    """
    def __init__(self, starer_playlist, starer_playlist_owner):
        self.numPlaylists = 0
        self.vertList = {}
        self.playlist_owner = {starer_playlist: starer_playlist_owner}

    def __getitem__(self, node):
        """Allows access of the graph as a dictionary"""
        return self.vertList[node]

    def __contains__(self, node):
        """Checks if node is contained in any of the vertices"""
        return (node in self.vertList.keys()) | (node in self.vertList.values())

    def add_nodes(self, nodes_full, parent):
        assert isinstance(nodes_full, list)

        # get rid of any playlists/artists that we have already seen
        nodes = []
        for node in nodes_full:
            if node not in self:
                nodes.append(node)

        self.vertList[parent] = nodes

    def add_playlist_owner(self, playlists, owners):
        assert isinstance(playlists, list)
        assert isinstance(owners, list)
        assert len(owners) == len(playlists)

        for playlist, owner in zip(playlists, owners):
            self.playlist_owner[playlist] = owner

    def is_playlist(self, node):
        return node in self.playlist_owner.keys()

    @property
    def nodes(self):
        return self.vertList

    @property
    def depth(self):
        return len(self.playlist_owner.keys())