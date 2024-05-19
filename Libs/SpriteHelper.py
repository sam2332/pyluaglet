
import pyglet
import os
from Libs.DotNotationDict import DotNotationDict
def load_tiles():
    tiles = {}
    base_path = 'tiles'
    for folder in os.listdir(base_path):
        tiles[folder] = {}
        for filename in os.listdir(f'{base_path}/{folder}'):
            if filename.endswith('.png'):
                tile_name = os.path.splitext(filename)[0]
                tile_image = pyglet.image.load(f'{base_path}/{folder}/{filename}')
                tile_image.width = 32
                tile_image.height = 32
                tiles[folder][tile_name] = tile_image
    return DotNotationDict(tiles)