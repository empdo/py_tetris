import pyglet
from pyglet import shapes
from pyglet.graphics import draw

batch = pyglet.graphics.Batch()

window = pyglet.window.Window(600, 600, "tetris")
block_size = 32

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



class Board:
    def __init__(self):
        self.grid = [[(74, 74, 74) for x in range(10)] for x in range(16)] 
        self.current_block = Block("I", (55, 55, 255));
        self.create_bundle()
    
    def draw_board(self):
        for i, _i in enumerate(self.grid):
            for j, _j in enumerate(self.grid[i]):
                square = shapes.Rectangle(block_size, block_size, (j*block_size), (i*block_size), color=(self.grid[i][j]), batch=batch)
                print(self.grid[i][j])
        batch.draw()

    def spawn_block(self):
        for i, _i in enumerate(self.current_block.block_type["shapes"][0]):
            for j, _j in enumerate(_i):
                if _j != ".":
                    self.grid[i][j] = self.current_block.color
        self.draw_board()

    def create_bundle(self):
        pass

    def rotate():
        pass


board = Board()

@window.event
def on_draw():
    window.clear()
    board.spawn_block()

pyglet.app.run()
