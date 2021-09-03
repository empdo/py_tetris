import pyglet

from pyglet.window import key
from pyglet.gl import *

from .import Board, placed_blocks

background = pyglet.graphics.OrderedGroup(0)
window = pyglet.window.Window(480, 600, "tetris")

drop_time = 0.7

hold_text = []

board = Board()

@window.event
def on_key_press(symbol, modifiers):
    global drop_time

    if symbol == key.LEFT:
        board.block_side(-1)
    elif symbol == key.RIGHT:
        board.block_side(1)
    elif symbol == key.UP:
        board.piece_rotate()
    elif symbol == key.DOWN:
        drop_time = 0.2
    elif symbol == key.SPACE:
        board.hard_drop_block()
    elif symbol == key.C:
        board.hold_block()


@window.event
def on_key_release(symbol, modifiers):
    global drop_time

    if symbol == key.DOWN:
        drop_time = 0.7


@window.event
def on_draw():
    window.clear()

    #colors = [(235, 64, 52, 200), (235, 223, 52, 205), (52, 235, 58, 205), (38, 60, 255, 205), (215, 38, 255, 205)]

    #for index, letter in enumerate("HOLD"):
    pyglet.shapes.BorderedRectangle(
    340, 420, 125, 100, 4,(41, 40, 40), div_vec((41, 40, 40), 2) ).draw()
    (pyglet.text.Label("NEXT",
            font_name='Open Sans',
            font_size=22,
            bold=True,
            x=402.5, y=540,
            color= (255, 255, 255, 255),
            anchor_x='center', anchor_y='center')).draw()

    pyglet.shapes.BorderedRectangle(
    340, 250, 125, 100, 4,(41, 40, 40), div_vec((41, 40, 40), 2) ).draw()
    (pyglet.text.Label("HOLD",
            font_name='Open Sans',
            font_size=22,
            bold=True,
            x= 402.5, y=370,
            color= (255, 255, 255, 255),
            anchor_x='center', anchor_y='center')).draw()
    

    board.update_board()

def div_vec(vec: tuple[int, ...], scalar: int):
    return *map(lambda x: x // scalar, vec),





def update_frames(var):
    positions = board.current_block.position
    if (board.current_block != None):
        if board.can_move(-1, 0):
            board.block_down()
        else:
            for i in positions:
                placed_blocks[i[0]][i[1]] = board.current_block.color

    if(len(board.queue) <= 2):
        board.create_bundle()

    board.update_board()

pyglet.clock.schedule_interval(update_frames, drop_time)

pyglet.app.run()
