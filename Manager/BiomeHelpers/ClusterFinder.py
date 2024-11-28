class ClusterFinder:
    def __init__(self, biome_map):
        self.biome_map = biome_map
        self.visited = set()  # Set für besuchte Positionen
        self.clusters = []  # Liste für alle gefundenen Cluster

    def floodfill(self):
        """
        Führt Flood-Fill durch, um alle Cluster in der Karte zu finden.
        """
        for x in range(self.biome_map.shape[0]):
            for y in range(self.biome_map.shape[1]):
                if (x, y) not in self.visited:
                    # Neues Cluster starten
                    cluster = self.floodfill_recursive(x, y)
                    if cluster:
                        self.clusters.append(cluster)
        self.clusterDict = {}
        id = 0
        for cluster in self.clusters:
            self.clusterDict[self.biome_map[cluster[0][0], cluster[0][1]]][id] = cluster
        print(self.clusterDict)
        return self.clusterDict

    def get_neighbours(self, x, y):
        """
        Gibt gültige Nachbarn einer Zelle zurück (innerhalb der Karte).
        """
        neighbours = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1)
        ]
        return [
            (nx, ny) for nx, ny in neighbours
            if 0 <= nx < self.biome_map.shape[0] and 0 <= ny < self.biome_map.shape[1]
        ]

    def floodfill_recursive(self, x, y):
        """
        Rekursiver Flood-Fill-Algorithmus für zusammenhängende Bereiche.
        """
        biome_type = self.biome_map[x, y]
        current_cluster = set()
        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()

            if (cx, cy) in self.visited:
                continue

            self.visited.add((cx, cy))
            current_cluster.add((cx, cy))

            for nx, ny in self.get_neighbours(cx, cy):
                if (nx, ny) not in self.visited and self.biome_map[nx, ny] == biome_type:
                    stack.append((nx, ny))

        return current_cluster