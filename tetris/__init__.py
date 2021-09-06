from .shapes import *

import copy
import random
from pprint import pprint
#import numpy as np

import pyglet
from pyglet import media
from pyglet.graphics import draw, Batch
import pyglet.text


batch = Batch()

# VARIABLES
block_size = 32
ui_offset = 50
bg_color = (40, 0, 41)
ghost_block_color = (63, 46, 64)

scores = (0, 100, 200, 300, 800)

width, heigth = 9, 20

default_grid = [[bg_color for x in range(
    width + 1)] for x in range(heigth + 1)]


# BLOCKS
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
    def __init__(self, block: dict, color: tuple[int, ...]):
        self.block = block["shapes"][0]
        self.block_name = block
        self.color = color
        self.blocks = []

    def draw_holder(self):
        offset = 323
        if self.color == (0, 255, 255):
            offset -= block_size - 15

        for x, row in enumerate(self.block):
            for y, column in enumerate(row):
                if column != ".":
                    self.blocks.append(
                        pyglet.shapes.BorderedRectangle(
                            offset + 17 + x*(block_size - 6), ui_offset + 183 + y*(block_size-6), block_size - 8, block_size - 8, 4, div_vec(self.color, 2), self.color, batch=batch)
                    )


class Next:
    def __init__(self, block: dict, color: tuple[int, ...]):
        self.block = block["shapes"][0]
        self.block_name = block
        self.color = color
        self.blocks = []

    def draw_holder(self):
        offset = 323
        if self.color == (0, 255, 255):
            offset -= block_size - 15

        for x, row in enumerate(self.block):
            for y, column in enumerate(row):
                if column != ".":
                    self.blocks.append(
                        pyglet.shapes.BorderedRectangle(
                            offset + 17 + x*(block_size - 6), ui_offset + 356 + y*(block_size-6), block_size - 8, block_size - 8, 4, div_vec(self.color, 2), self.color, batch=batch)
                    )


class Block:
    def __init__(self, block_type: str, color: tuple[int, ...]):
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
                    _position.append([heigth - (i+2), width // 2 + j - 2, _j])

        return _position

    def rotate_pos(self, placed_blocks):
        _position = []
        _rotation = self.rotation

        # get rotation point
        for position in self.position:
            if "1" in position:
                rotation_point = position

        _position.append(rotation_point)
        _rotation = (self.rotation + 1) % len(self.block_type["shapes"])

        """
        Calculates the new position from every block out of the rotation point,
        Results in the position for the next rotation
        """
        for y, row in enumerate(self.block_type["shapes"][_rotation]):
            for x, column in enumerate(row):
                if column not in [".", "1"]:
                    _position.append(
                        [rotation_point[0] + (2 - y), rotation_point[1] - (2 - x), column])


        can_rotate = self.can_rotate(_position, rotation_point, placed_blocks)
        if can_rotate[0] or can_rotate[1] != 0:
            for i in _position:
                i[1] += can_rotate[1]
            self.position = _position
            self.rotation = _rotation

    """
    Checks if any block is outside of map, 0>x>10
    Checks if any block is in another block, with the kickback if any block was outside
    Checks if any block is in another block after compensating with kickback

    If any block is in another block, return that it should not turn, [False, 0]
    If no blocks are in any other block, return that it should turn [True, 0]... 
    ...if it does not have any kickback, if it does, return that it should turn with kickback, [False, kickback]

    """
    def can_rotate(self, position: list[tuple[int, ...]], rotation_point: tuple[int, ...], placed_blocks):
        blocks_outside = 0
        blocks_in_rigth = 0
        blocks_in_left = 0

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

        diff_to_return = 0
        if (blocks_in_left != 0 and blocks_in_rigth == 0 and blocks_outside == 0):
            diff_to_return = blocks_in_left
        elif (blocks_in_rigth != 0 and blocks_in_left == 0 and blocks_outside == 0):
            diff_to_return = -blocks_in_rigth
        elif blocks_outside != 0 and blocks_in_left == 0 and blocks_in_rigth == 0:
            diff_to_return = blocks_outside

        for pos in position:
            if pos[0] < 0 or pos[1] + diff_to_return < 0 or pos[1] + diff_to_return > width or placed_blocks[pos[0]][pos[1] + diff_to_return] != None:
                return[False, 0]

        if blocks_outside == 0 and blocks_in_rigth == 0 and blocks_in_left == 0:
            return([True, 0])

        return([False, diff_to_return])


class Board:
    def __init__(self):
        self.init_game()
        self.spawn_block()

    # draws the board from grid 🤯
    def draw_board(self):
        for y, row in enumerate(self.placed_blocks):
            for x, block_color in enumerate(row):
                color = block_color if block_color != None else bg_color

                self.blocks.append(
                    self.create_shape([y, x], color)
                )
        if self.current_block:
            positions = self.lowest_block_position()
            for position in positions:
                self.create_shape(position, ghost_block_color)

        for position in self.current_block.position:
            self.create_shape(position, self.current_block.color)

        batch.draw()

    def create_shape(self, position: tuple[int, ...], color: tuple[int, ...]):
        self.blocks.append(
            pyglet.shapes.BorderedRectangle(
                2 + position[1]*block_size, 2 + position[0]*block_size, block_size - 2, block_size - 2, 4, div_vec(color, 2), color, batch=batch)
        )
    """
    Adds level when cleard enough lines
    """
    def update_board(self):

        if self.cleared_lines >= max(100, (self.level * 10 - 50)) or self.cleared_lines >= (self.level * 10 + 10):
            self.level += 1

        self.draw_board()

    def resume_game(self):
        self.is_paused = False


    """
    Finds the lowest posible y value for the current tetremino,
    returns it
    """
    def lowest_block_position(self):

        block_positions = self.current_block.position

        i = 0
        while self.can_move(i, 0):
            i -= 1

        return [[pos[0] + i + 1, pos[1]] for pos in block_positions]


    """
    Moves the block down until it can't,
    Adds the block to placed blocks, spawns a new one
    """
    def hard_drop_block(self):
        while self.can_move(-1, 0):
            self.block_down()

        for block_position in self.current_block.position:
            self.placed_blocks[block_position[0]][block_position[1]
                                             ] = self.current_block.color

        self.spawn_block()
    
    """
    Checks every line, is it full, then...
    ...remove it and insert a empty line at the top of the placed block grid
    """
    def check_lines(self):
        number_of_rows = 0
        rows = []
        for row in self.placed_blocks:
            if all(row):
                number_of_rows += 1
                rows.append(row)

        for line in rows:
            self.clear_line(line)
            self.cleared_lines += 1

        self.score += scores[number_of_rows] #TODO: multiplicera med level

    def clear_line(self, line):
        self.placed_blocks.remove(line)
        self.placed_blocks.insert(16, [None for x in range(width + 1)])


    """
    Checks line, if there are any completed ones
    If the queue has one or less tetremino in it, create a new bundle
    Set current block to the first one in the queue,
    Set the second block in the quee to be visible in the next container
    """
    def spawn_block(self):
        self.check_lines()
        if (len(self.queue) <= 1):
            self.create_bundle()

        self.current_block = Block(self.queue[0][0], self.queue[0][1])
        self.queue.pop(0)

        self.next = Next(blocks[self.queue[0][0]], self.queue[0][1])
        self.next.draw_holder()

        self.update_board()

    """
    Loops through every block inte the current tetremino,
    lowers the blocks y value by one
    """
    def block_down(self):
        positions = self.current_block.position
        for i in positions:
            i[0] -= 1

    """
    Delta_x: either 1 or -1 depending on the side to go,
    Changes every blocks x value by delta_x
    """
    # TODO: change name
    def block_side(self, delta_x: int):
        positions = self.current_block.position
        if self.can_move(0, delta_x):
            for block in positions:
                block[1] += delta_x

    def piece_rotate(self):
        self.current_block.rotate_pos(self.placed_blocks)

    """
    Adds the change in the x and y from delta_x, delta_y
    Checks if the position is occupied or outside of the map 
    """
    def can_move(self, delta_x: int, delta_y: int):
        for block in self.current_block.position:
            x = block[0] + delta_x
            y = block[1] + delta_y

            if x < 0 or y < 0 or y > width:
                return False

            if self.placed_blocks[x][y] != None:
                return False

        return True

    def hold_block(self):
        _current_block = self.current_block
        self.holder = Holder(self.current_block.block_type,
                             self.current_block.color)

        if self.stashed_block is None:
            self.spawn_block()
        else:
            self.current_block = self.stashed_block
            self.current_block.position = self.current_block.default_pos()

        self.stashed_block = _current_block
        self.update_board()

        self.holder.draw_holder()


    """
    Create a copy of the block list, shuffles if
    Adds the content of the list to the block queue
    """
    def create_bundle(self):
        # scramble _blocks
        _blocks = [[str(block), blocks[block]["color"]] for block in blocks]

        random.shuffle(_blocks)

        for block in _blocks:
            self.queue.append(block)

    """
    Pause game
    """
    def pause_game(self):
        self.is_paused = not self.is_paused

    def init_game(self):
        self.current_block = None
        self.placed_blocks = [[None for x in range(width + 1)] for x in range(heigth + 1)]
        self.blocks = []
        self.score = 0
        self.level = 0
        self.cleared_lines = 0

        self.is_paused = False

        self.queue = []
        self.holder = None
        self.stashed_block = None
        self.next = None
        self.spawn_block()

def div_vec(vec: tuple[int, ...], scalar: int):
    return *map(lambda x: x // scalar, vec),
