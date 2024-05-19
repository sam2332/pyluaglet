from array import array
import random
import pyglet
import arcade
from arcade import gl

window = pyglet.window.Window(720, 720)
ctx = gl.Context(window)
print("OpenGL version:", ctx.gl_version)

size = window.width // 4, window.height // 4

def gen_initial_data(width, height):
    dx, dy = window.height / width, window.width / height
    for y in range(height):
        for x in range(width):
            # current pos
            # yield window.width // 2
            # yield window.height // 2
            yield x * dx + dx / 2
            yield y * dy + dy / 2
            # desired pos
            yield x * dx + dx / 2
            yield y * dy + dy / 2


def gen_colors(width, height):
    for _ in range(width * height):
        yield random.uniform(0, 1) 
        yield random.uniform(0, 1) 
        yield random.uniform(0, 1) 

buffer1 = ctx.buffer(data=array('f', gen_initial_data(*size)))
buffer2 = ctx.buffer(reserve=buffer1.size)
colors = ctx.buffer(data=array('f', gen_colors(*size)))

geometry1 = ctx.geometry([
    gl.BufferDescription(buffer1, '2f 2x4', ['in_pos']),
    gl.BufferDescription(colors, '3f', ['in_color']),
])
geometry2 = ctx.geometry([
    gl.BufferDescription(buffer2, '2f 2x4', ['in_pos']),
    gl.BufferDescription(colors, '3f', ['in_color']),
])

transform1 = ctx.geometry([gl.BufferDescription(buffer1, '2f 2f', ['in_pos', 'in_dest'])])
transform2 = ctx.geometry([gl.BufferDescription(buffer2, '2f 2f', ['in_pos', 'in_dest'])])

# Is there a way to make ortho projection in pyglet?
projection = arcade.create_orthogonal_projection(0, window.width, 0, window.height, -100, 100).flatten()

points_program = ctx.program(
    vertex_shader="""
    #version 330

    uniform mat4 projection;
    in vec2 in_pos;
    in vec3 in_color;
    out vec3 color;

    void main() {
        gl_Position = projection * vec4(in_pos, 0.0, 1.0);
        color = in_color;
    }
    """,
    fragment_shader="""
    #version 330

    in vec3 color;
    out vec4 fragColor;

    void main() {
        fragColor = vec4(color, 1.0);
    }
    """,
)
points_program['projection'] = projection

transform_program = ctx.program(
    vertex_shader="""
    #version 330

    uniform float dt;
    uniform vec2 mouse_pos;

    in vec2 in_pos;
    in vec2 in_dest;

    out vec2 out_pos;
    out vec2 out_dest;

    void main() {
        out_dest = in_dest;
        // Slowly move the point towards the desired location
        vec2 dir = in_dest - in_pos;
        vec2 pos = in_pos + dir * dt;
        // Move the point away from the mouse position
        float dist = length(pos - mouse_pos);
        if (dist < 60.0) {
            pos += (pos - mouse_pos) * dt * 10;
        }
        out_pos = pos;
    }
    """,
)
frame_time = 0
mouse_pos = -100, -100


@window.event
def on_draw():
    global buffer1, buffer2, geometry1, geometry2, transform1, transform2
    window.clear()
    ctx.point_size = 2

    geometry1.render(points_program, mode=gl.POINTS)
    transform_program['dt'] = frame_time
    transform_program['mouse_pos'] = mouse_pos
    transform1.transform(transform_program, buffer2)

    buffer1, buffer2 = buffer2, buffer1
    geometry1, geometry2 = geometry2, geometry1
    transform1, transform2 = transform2, transform1


def update(dt):
    global frame_time
    frame_time = dt


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos
    mouse_pos = x, y


if __name__ == '__main__':
    pyglet.clock.schedule(update)
    pyglet.app.run()