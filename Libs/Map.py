
# Map class

def load_tiles(game, tileset, tile_width, tile_height):
    tiles = {}
    for tile in tileset:
        img = pyglet.resource.image(tileset[tile])
        img.width = tile_width
        img.height = tile_height
        tiles[tile] = CustomSprite(img, walkable=True)
    return tiles
def define_map(game, tiles, width, height, tileset, default_tile='grass', map_data=None):
    tiles = load_tiles
    class Map:
        def __init__(self, tiles, width, height, default_tile='grass'):
            self.tiles = tiles
            self.width = width
            self.height = height
            self.map_data = [[tiles[default_tile] for _ in range(height)] for _ in range(width)]
            if map_data:
                for x, y, tile in map_data:
                    if tile is not None and tile in tiles and tile != 0:
                        self.map_data[x][y] = tiles[tile]
        def draw(self):
            for x in range(self.width):
                for y in range(self.height):
                    tile = self.map_data[x][y]
                    tile.set_position(x * tile.width, y * tile.height)
                    tile.draw()

        def is_walkable(self, x, y):
            if 0 <= x < self.width and 0 <= y < self.height:
                return self.map_data[x][y].walkable
            return False
    return Map