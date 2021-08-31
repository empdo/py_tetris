from shapes import *
import pyglet
import copy
import random

from pyglet import shapes
from pyglet.window import key
from pyglet.graphics import draw
from pyglet.gl import *

batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
window = pyglet.window.Window(600, 600, "tetris")


block_size = 32
bg_color = (16, 0, 20)

width, heigth = 10, 20

default_grid = [[bg_color for x in range(width +1)] for x in range(heigth +1)]
placed_blocks = []
drop_time = 0.7

# shapes

# blocks
blocks = {
    "I": {
        "shapes": I,
        "color": (0, 255, 255)
    },
    "S": {
        "shapes": S,
        "color": (255, 0, 0)
    },
    "L":
        {
            "shapes": L,
            "color": (255, 127, 0)
    },
    "J": {
        "shapes": J,
        "color": (0, 0, 255)
    },
    "Z": {
        "shapes": Z,
        "color": (0, 255, 0)
    },
    "T": {
        "shapes": T,
        "color": (128, 0, 128)
    },
    "O": {
        "shapes": O,
        "color": (255, 255, 0)
    }
}


class Block:
    def __init__(self, block_type, color):
        self.block_type = blocks[block_type]
        self.rotation = 0
        self.color = color
        self.position = self.default_pos()

    # setts default position of block
    def default_pos(self):
        _position = []

        for i, _i in enumerate(self.block_type["shapes"][0]):
            for j, _j in enumerate(_i):
                if _j != ".":
                    _position.append([heigth - (i+2), j, _j])

        return _position

    def rotate_pos(self):
        _position = []
        _rotation = self.rotation

        # get rotation point
        for position in self.position:
            if "1" in position:
                rotation_point = position

        # clear positions and add one to the rotation
        _position.append(rotation_point)
        _rotation = (self.rotation + 1) % len(self.block_type["shapes"])

        # set varje block till diffrensen i position från rotation point + rotaion point eller något jag behöver mer hjärnceller
        for i, _i in enumerate(self.block_type["shapes"][_rotation]):
            for j, _j in enumerate(_i):
                if _j not in [".", "1"]:
                    _position.append(
                        [rotation_point[0] - (2 - i), rotation_point[1] - (2 - j), _j])

        can_rotate = self.can_rotate(_position, rotation_point)
        if can_rotate[0] or can_rotate[1] != 0:
            for i in _position:
                i[1] += can_rotate[1]
            self.position = _position
            self.rotation = _rotation

    def can_rotate(self, position, rotation_point):
        blocks_outside = 0
        blocks_in_rigth = 0
        blocks_in_left = 0

        # Returna false om de inte fungerar men med en diff på om blocket \
        # kan och behöver flytta sig åt sidan om den är utanför eller i ett annat block

        for block_position in position:
            if (block_position[1] < 0):
                blocks_outside += 1
            elif (block_position[1] > width -1):
                blocks_outside -= 1

        for block_position in position:
            for placed_block_position in placed_blocks:
                if ((block_position[0], block_position[1] + blocks_outside) == (placed_block_position[0], placed_block_position[1])):
                    if(block_position[1] > rotation_point[1]):
                        blocks_in_rigth += 1
                    else:
                        blocks_in_left += 1

        if (blocks_in_left != 0 and blocks_in_rigth != 0):
            return([False, 0])
        elif (blocks_in_left != 0):
            return([False, blocks_in_left])
        elif (blocks_in_rigth != 0):
            return([False, -blocks_in_rigth])
        elif blocks_outside != 0:
            return([False, blocks_outside])
        else:
            return([True, 0])


# TODO: fixa småfel
# TODO: veta om det är bra eller dåligt med tre miljarder funktioner

class Board:
    def __init__(self):
        self.grid = default_grid
        self.current_block = None
        self.placed_blocks = []
        self.blocks = []
        self.queue = []
        self.spawn_block()

    # draws the board from grid 🤯
    def draw_board(self):
        for i, _i in enumerate(self.grid):
            for j, _j in enumerate(self.grid[i]):
                self.blocks.append(shapes.Rectangle(
                    j*block_size, i*block_size, block_size -2, block_size -2, color=(self.grid[i][j]), batch=batch))

        batch.draw()

    # makes a blank board, sets the current block then the placed blocks
    def update_board(self):

        if self.current_block:
            self.grid = copy.deepcopy(default_grid)
            for i in self.current_block.position:
                self.grid[i[0]][i[1]] = self.current_block.color
            for i in placed_blocks:
                self.grid[i[0]][i[1]] = i[2]


        self.draw_board()

    def check_lines(self):
        count = 0

        for n in range(16):
            count = 0
            for i, _i in enumerate(placed_blocks):
                if _i[0] == n:
                    count += 1
                if count == 10:
                    self.clear_line(_i[0])

    def lowest_block_point(self):
        pass
    def hard_drop_block(self):
        while self.can_move(-1, 0):
            self.block_down()

    def clear_line(self, line):
        pass
        #        print(placed_blocks)
        #        for i, _i in enumerate(placed_blocks):
        #            if _i[0] == line:
        #                placed_blocks.remove(_i)
        #
       # for i, _i in enumerate(placed_blocks):
       #         if _i[0] > line:
       #             placed_blocks[i][0] -= 1

        # spawn block, will probably do more

    def spawn_block(self):
        if (len(self.queue) <= 1):
            self.create_bundle()

        self.current_block = Block(self.queue[0][0], self.queue[0][1])
        self.queue.pop(0)

        self.update_board()

    def block_down(self):
        positions = self.current_block.position
        if self.can_move(-1, 0):
            for i in positions:
                i[0] -= 1
        else:
            for i in positions:
                placed_blocks.append([i[0], i[1], self.current_block.color])
            self.spawn_block()

        self.update_board()

    # TODO: change name
    def block_side(self, change):
        positions = self.current_block.position
        if self.can_move(0, change):
            for i in positions:
                i[1] += change

    def piece_rotate(self):
        self.current_block.rotate_pos()

    def can_move(self, delta_x, delta_y):
        for i in self.current_block.position:
            x = i[0] + delta_x
            y = i[1] + delta_y

            if x < 0 or y < 0 or y > width:
                return False
            for i in placed_blocks:
                if i[0] == x and i[1] == y:
                    return False

        return True

    def can_rotate():
        pass

    # creates a bundle then adds it to queue
    def create_bundle(self):
        # scramble _blocks
        _blocks = [[str(i), blocks[i]["color"]] for i in blocks]

        random.shuffle(_blocks)

        for i in _blocks:
            self.queue.append(i)

    def rotate():
        pass


board = Board()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        board.block_side(-1)
    elif symbol == key.RIGHT:
        board.block_side(1)
    elif symbol == key.UP:
        board.piece_rotate()
    elif symbol == key.D:
        board.hard_drop_block()


@window.event
def on_draw():
    window.clear()
    board.update_board()


def update_frames(var):
    if board.current_block != None:
        board.block_down()

    if(len(board.queue) <= 2):
        board.create_bundle()


pyglet.clock.schedule_interval(update_frames, drop_time)

pyglet.app.run()
