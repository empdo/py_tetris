from .shapes import *

import copy
import random
from pprint import pprint

import pyglet
from pyglet.graphics import draw, Batch
import pyglet.text

batch = Batch()

#VARIABLES
block_size = 32
ui_offset = 50
bg_color = (40, 0, 41)
ghost_block_color = (63, 46, 64)

width, heigth = 9, 20

default_grid = [[bg_color for x in range(
    width + 1)] for x in range(heigth + 1)]

placed_blocks = [[None for x in range(width + 1)] for x in range(heigth +1)]

#BLOCKS
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

class Holder:
    def __init__(self, block, color):
        self.block = block["shapes"][0]
        self.color = color
        self.blocks = []

    def draw_holder(self):
        for x, row in enumerate(self.block):
            for y, column in enumerate(row):
                if column != ".":
                    self.blocks.append(
                        pyglet.shapes.BorderedRectangle(
                        15 + x*block_size, ui_offset + 275 + y*block_size, block_size - 2, block_size - 2, 4, div_vec(self.color, 2), self.color, batch=batch)
                    )


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
        for y, row in enumerate(self.block_type["shapes"][_rotation]):
            for x, column in enumerate(row):
                if column not in [".", "1"]:
                    _position.append(
                        [rotation_point[0] + (2 - y), rotation_point[1] - (2 - x), column])

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
            elif (block_position[1] > width):
                blocks_outside -= 1

        for block_position in position:
            if placed_blocks[block_position[0]][block_position[1] + blocks_outside] != None:
                if(block_position[1] > rotation_point[1]):
                    blocks_in_rigth += 1
                else:
                    blocks_in_left += 1

        print(blocks_outside, blocks_in_left, blocks_in_rigth)

        diff_to_return = 0
        if (blocks_in_left != 0 and blocks_in_rigth == 0 and blocks_outside == 0):
            diff_to_return = blocks_in_left
        elif (blocks_in_rigth != 0 and blocks_in_left == 0 and blocks_outside == 0):
            diff_to_return = -blocks_in_rigth
        elif blocks_outside != 0 and blocks_in_left == 0 and blocks_in_rigth == 0:
            diff_to_return = blocks_outside
        elif blocks_outside == 0 and blocks_in_rigth == 0 and blocks_in_left == 0:
            return([True, 0])

        return([False, diff_to_return])

# TODO: fixa småfel
# TODO: veta om det är bra eller dåligt med tre miljarder funktioner

class Board:
    def __init__(self):
        self.grid = default_grid
        self.current_block = None
        self.placed_blocks = []
        self.blocks = []

        self.queue = []
        self.holder = None
        self.stashed_block = None
        self.spawn_block()

    # draws the board from grid 🤯
    def draw_board(self):
        for y, row in enumerate(self.grid):
            for x, block_color in enumerate(row):
                self.blocks.append(
                    pyglet.shapes.BorderedRectangle(
                    150 + 2 + x*block_size, 2 + y*block_size, block_size - 2, block_size - 2, 4, div_vec(block_color, 2), block_color, batch=batch)
                )

        batch.draw()
    

    # makes a blank board, sets the current block then the placed blocks
    def update_board(self):

        if self.current_block:
            self.grid = copy.deepcopy(default_grid)
            self.check_lines()
            self.lowest_block_position()

            for i in self.current_block.position:
                self.grid[i[0]][i[1]] = self.current_block.color

            for x, row in enumerate(placed_blocks):
                for y, column in enumerate(row):
                        if column != None:
                            self.grid[x][y] = column

        self.draw_board()


    def lowest_block_position(self):
        block_positions = self.current_block.position

        i = 0
        while self.can_move(i, 0):
            i -= 1

        for position in block_positions:
            self.grid[position[0] + i + 1][position[1]] = ghost_block_color

    def hard_drop_block(self):
        while self.can_move(-1, 0):
            self.block_down()
        for block_position in self.current_block.position:
            placed_blocks[block_position[0]][block_position[1]] = self.current_block.color

        self.spawn_block()

    def check_lines(self):
        for x, row in enumerate(placed_blocks):
            count = 0
            for y, column in enumerate(row):
                if column != None:
                    count += 1
                if count == 10:
                    self.clear_line(x) 

    def clear_line(self, line):
        placed_blocks.pop(line)
        placed_blocks.insert(16, [None for x in range(width + 1)])

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
                placed_blocks[i[0]][i[1]] = self.current_block.color
                
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

            if placed_blocks[x][y] != None:
                return False

        return True

    def can_rotate():
        pass

    def hold_block(self):
        _current_block = self.current_block
        self.holder = Holder(self.current_block.block_type, self.current_block.color)

        if self.stashed_block is None:
            self.spawn_block()
        else:
            self.current_block = self.stashed_block

        self.stashed_block = _current_block
        self.update_board()


        self.holder.draw_holder()


    # creates a bundle then adds it to queue
    def create_bundle(self):
        # scramble _blocks
        _blocks = [[str(i), blocks[i]["color"]] for i in blocks]

        random.shuffle(_blocks)

        for i in _blocks:
            self.queue.append(i)

    def rotate():
        pass

def div_vec(vec: tuple[int, ...], scalar: int):
    return *map(lambda x: x // scalar, vec),