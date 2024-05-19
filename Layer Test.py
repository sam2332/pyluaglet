import pyglet
from pyglet.window import key
import time
from Libs.SpriteHelper import load_tiles

# Create a window
window = pyglet.window.Window(width=800, height=600, caption="Layer Test")

# Load all sprites initially
sprites = load_tiles()

# Layers
layers = {
    'background': [],
    'decorations': [],
    'middleground': [],
    'foreground': []
}
cache_layers = {
    'background': None,
    'decorations': None,
    'middleground': None,
    'foreground': None
}

# Variables to track position
tile_size = 32  # Assuming each tile is 32x32 pixels
cols = window.width // tile_size
rows = window.height // tile_size
margin_bottom = 5
margin_left = 10
header_height = 20

# Refresh interval
refresh_interval = 60  # in seconds
time_since_refresh = time.time()
print(sprites)
# Example sprite types (adjust these according to your actual sprite types)
grass_sprite = sprites['terrain.grass']
tree_sprite = sprites['obstacles.tree']
rock_sprite = sprites['obstacles.rock']
sign_sprite = sprites['obstacles.sign']
player_sprite = sprites['player.idle']

# Fill the background with grass
for row in range(rows):
    for col in range(cols):
        layers['background'].append((grass_sprite, col * tile_size, row * tile_size))

# Add a few trees and rocks
layers['decorations'].append((tree_sprite, 5 * tile_size, 5 * tile_size))
layers['decorations'].append((tree_sprite, 10 * tile_size, 8 * tile_size))
layers['decorations'].append((rock_sprite, 15 * tile_size, 3 * tile_size))
layers['decorations'].append((rock_sprite, 20 * tile_size, 12 * tile_size))

# Add a sign at the center
sign_x = (window.width // 2) - (tile_size // 2)
sign_y = (window.height // 2) - (tile_size // 2)
layers['middleground'].append((sign_sprite, sign_x, sign_y))

# Add the player at the bottom center
player_x = (window.width // 2) - (tile_size // 2)
player_y = tile_size  # Bottom of the screen
layers['foreground'].append((player_sprite, player_x, player_y))

@window.event
def on_draw():
    global time_since_refresh, sprites

    if time.time() - time_since_refresh > refresh_interval:
        sprites = load_tiles()
        time_since_refresh = time.time()
        # Reload layers if sprites are updated
        layers['background'] = [(grass_sprite, col * tile_size, row * tile_size)
                                for row in range(rows) for col in range(cols)]
        cache_layers['background'] = None

    window.clear()

    # Draw each layer
    for layer_name in ['background', 'decorations', 'middleground', 'foreground']:
        if not cache_layers[layer_name]:
            # Render sprites to a transparent background canvas and cache it
            batch = pyglet.graphics.Batch()
            for item in layers[layer_name]:
                sprite, x, y = item
                sprite.blit(x, y, batch=batch)
            cache_layers[layer_name] = batch
        cache_layers[layer_name].draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        window.close()

if __name__ == "__main__":
    pyglet.app.run()
