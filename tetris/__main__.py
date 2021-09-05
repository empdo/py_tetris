import pyglet

from pyglet.window import key
from pyglet.gl import *
from pyglet import font, shapes, resource

from .import Board, placed_blocks
from pathlib import Path

background = pyglet.graphics.OrderedGroup(0)
window = pyglet.window.Window(485, 600, "tetris")

resource.add_font(Path(__file__).parent/"font.ttf")
font.load("Karmatic Arcade")

drop_time = 0.7

hold_text = []

def div_vec(vec: tuple[int, ...], scalar: int):
    return *map(lambda x: x // scalar, vec),

class Menu:
    def __init__(self, *options: str):
        self.current_option = 0
        self._options = options

    @property
    def options(self):
        list = [shapes.BorderedRectangle(
        60, 100, 200, 400, 8,(200, 200, 200), div_vec((0,0,0),1))]

        text_options = {"font_name": 'Karmatic Arcade', "font_size": 18, "color":(0,0,0, 255), "anchor_x":'center', "anchor_y":'center', "bold":True}
    
        for index, option in enumerate(self._options):
            list.append(
                (pyglet.text.Label(option.upper() if index is self.current_option else option.lower(),
                        **text_options,
                        #underline = (0,0,0, 255),
                        x=160, y= ((265 + (len(self._options) * 35)) - index * 35)
                ))
            )

        return list


    

board = Board()
menu = Menu("resume", "restart", "options")


@window.event
def on_key_press(symbol, modifiers):
    global drop_time

    if (not board.is_paused):
        if symbol == key.LEFT:
            move_left(None)
        elif symbol == key.RIGHT:
            move_right(None)
        elif symbol == key.UP:
            board.piece_rotate()
        elif symbol == key.DOWN:
            drop_time = 0.05
        elif symbol == key.SPACE:
            board.hard_drop_block()
        elif symbol == key.C:
            board.hold_block()

    if symbol == key.P:
        board.pause_game()
    elif symbol == key.UP:
        menu.current_option = (menu.current_option -1 ) % (len(menu.options) -1)
    elif symbol == key.DOWN:
        menu.current_option = (menu.current_option +1 ) % (len(menu.options) -1)

@window.event
def on_key_release(symbol, modifiers):
    global drop_time
    if symbol == key.DOWN:
        drop_time = 0.7
    elif symbol == key.RIGHT:
        pyglet.clock.unschedule(move_right)
    elif symbol == key.LEFT:
        pyglet.clock.unschedule(move_left)

def move_right(var):
    board.block_side(1)
    #pyglet.clock.schedule_once(move_right, 1/4)

def move_left(var):
    board.block_side(-1)
    #pyglet.clock.schedule_once(move_left, 1/4)



@window.event
def on_draw():
    window.clear()

    #colors = [(235, 64, 52, 200), (235, 223, 52, 205), (52, 235, 58, 205), (38, 60, 255, 205), (215, 38, 255, 205)]

    #for index, letter in enumerate("HOLD"):

    text_options = {"font_name": 'Karmatic Arcade', "font_size":18, "color":(255, 255, 255, 255), "anchor_x":'center', "anchor_y":'center', "bold":True}

    pyglet.shapes.BorderedRectangle(
    340, 420, 125, 100, 8,(41, 0, 40), div_vec((41, 0, 40), 2) ).draw()

    (pyglet.text.Label("NEXT",
            x=402.5, y=540,
            **text_options        
            )).draw()
    (pyglet.text.Label("NEXT",
            x=403.5, y=539,
            **text_options       
            )).draw()

    pyglet.shapes.BorderedRectangle(
    340, 250, 125, 100, 8,(41, 0, 40), div_vec((41, 0, 40), 2) ).draw()
    (pyglet.text.Label("HOLD",
            **text_options,
            x= 402.5, y=370)).draw()
    
    (pyglet.text.Label("SCORE:",
            **text_options,
            x= 402.5, y=210)
            ).draw()

    (pyglet.text.Label(str(board.score),
            **text_options,
            x= 402.5, y=180
    )).draw()

    (pyglet.text.Label("LEVEL:",
            **text_options,
            x= 402.5, y=140)
            ).draw()

    (pyglet.text.Label(str(board.level),
            **text_options,
            x= 402.5, y=110
    )).draw()

    board.update_board()

    if board.is_paused:
        shapes.BorderedRectangle(
        60, 100, 200, 400, 8,(200, 200, 200), div_vec((0,0,0),1)).draw()

        for option in menu.options:
            option.draw()





def update_frames(var):

    if not board.is_paused:
        positions = board.current_block.position
        if (board.current_block != None):
            if board.can_move(-1, 0):
                board.block_down()
            else:
                for i in positions:
                    placed_blocks[i[0]][i[1]] = board.current_block.color
                board.spawn_block()
        if(len(board.queue) <= 2):
            board.create_bundle()

    board.update_board()

    pyglet.clock.schedule_once(update_frames, drop_time)


update_frames("")

pyglet.app.run()
