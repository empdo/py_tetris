from ctypes import Array
import pyglet
from pyglet import shapes
from pyglet.graphics import draw
from pyglet.gl import *

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)

window = pyglet.window.Window(600, 600, "tetris")
block_size = 32

default_grid = [[(255, 229, 158) for x in range(10)] for x in range(16)]

S = [
    [
        ".....",
        "..00.",
        ".01..",
        ".....",
        "....."
    ],
    [
        ".....",
        ".0...",
        ".01..",
        "..0..",
        ".....",
    ],
]

I = [
    [
        "..0..",
        "..0..",
        "..1..",
        "..0..",
        "..0..",
    ],
    [
        ".....",
        ".....",
        "00100",
        ".....",
        ".....",
    ],

]

blocks = {
    "S": {
        "shapes": S,
        "color": (55, 55, 255)
    },
    "I": {
        "shapes": I,
        "color": (55, 55, 255)
    }

}


class Block:
    def __init__(self, block_type, color):
        self.block_type = blocks[block_type]
        self.rotation = 0
        self.color = color
        self.position = self.default_pos()

    def default_pos(self):
        _position = []
        
        for i, _i in enumerate(self.block_type["shapes"][0]):
            for j, _j in enumerate(_i):
                if _j != ".":
                    _position.append([15 - i, j, _j])

        return _position


class Board:
    def __init__(self):
        self.grid = default_grid
        self.current_block = Block("I", (55, 55, 255))
        self.placed_blocks = []
        self.blocks = []

    def draw_board(self):
        for i, _i in enumerate(self.grid):
            for j, _j in enumerate(self.grid[i]):

                self.blocks.append(shapes.Rectangle(
                    j*block_size, i*block_size, block_size, block_size, color=(self.grid[i][j]), batch=batch))

                print(i, j, self.grid[i][j], block_size, block_size,
                      (j*block_size), (i*block_size))
        batch.draw()

    def update_board(self):
        self.grid = [[(255, 229, 158) for x in range(10)] for x in range(16)]
        for i in self.current_block.position:
            self.grid[i[0]][i[1]] = self.current_block.color

        self.draw_board()

    def spawn_block(self):
        self.update_board()        

    def block_down(self):
        # if new position not in placed_blocks
        positions = self.current_block.position
        for i in positions:
            i[0] -= 1

        self.update_board() 

    def create_bundle(self):
        pass

    def rotate():
        pass


board = Board()


@window.event
def on_draw():
    window.clear()
    board.spawn_block()


def update_frames(dt):
    board.block_down()


pyglet.clock.schedule_interval(update_frames, 0.7)

pyglet.app.run()
