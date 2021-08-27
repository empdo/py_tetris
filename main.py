import pyglet
from pyglet import shapes
from pyglet.libs.win32.constants import NULL
batch = pyglet.graphics.Batch()

window = pyglet.window.Window(600, 600, "tetris")
block_size = 32

S = [
    [
        ".....",
        ".....",
        "..00.",
        ".01..",
        "....."
    ],
    [
        ".....",
        ".0...",
        ".01.",
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
    def __init__(self, block_type):
        self.block_type = blocks[block_type]
        self.rotation = 0


class Board:
    def __init__(self):
        self.grid = [[(74, 74, 74) for x in range(10)] for x in range(16)] 
        self.current_block = NULL;
        self.create_bundle()
    
    def draw_board(self):
        for i, _i in enumerate(self.grid):
            for j, _j in enumerate(self.grid[i]):
                square = shapes.Rectangle(block_size, block_size, (j*block_size), (i*block_size), color=(self.grid[i][j]), batch=batch)
        batch.draw()

    def create_bundle(self):
        pass


board = Board()

@window.event
def on_draw():
    window.clear()
    board.draw_board()

pyglet.app.run()
