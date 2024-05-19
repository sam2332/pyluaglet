import pyglet
from pyglet.window import key
import os
from Libs.SpriteHelper import load_tiles

# Create a window
window = pyglet.window.Window(width=800, height=600, caption="Tile Viewer")
#set fps
pyglet.clock.set_fps_limit(5)


# Load all sprites
sprites = load_tiles()

# Variables to track position
tile_size = 32  # Assuming each tile is 32x32 pixels
cols = window.width // tile_size
margin_bottom = 5
margin_left = 10
header_height = 40
time_since_refresh = 0
refresh_interval = 5
import time

@window.event
def on_draw():
    global time_since_refresh,sprites
    if time.time() - time_since_refresh > refresh_interval:
        sprites = load_tiles()
        time_since_refresh = time.time()

    window.clear()
    y_offset = window.height - header_height  # Start drawing from the top of the window

    for tileset in sprites:
        # Draw the header
        pyglet.text.Label(tileset, font_name='Arial', font_size=12, x=margin_left, y=y_offset).draw()
        y_offset -= (header_height + margin_bottom)

        for i, tile in enumerate(sprites[tileset]):
            x = (i % cols) * tile_size + margin_left
            y = y_offset - (i // cols) * tile_size

            # Ensure the tile is drawn within the window bounds
            if y < 0:
                break

            sprites[tileset][tile].blit(x, y)

        # Adjust y_offset for the next tileset
        rows_used = (len(sprites[tileset]) + cols - 1) // cols  # Compute rows used by the current tileset
        y_offset -= (rows_used * tile_size + margin_bottom)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.ESCAPE:
        window.close()

if __name__ == "__main__":
    pyglet.app.run()
