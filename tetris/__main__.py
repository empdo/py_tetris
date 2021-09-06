import pyglet
from pyglet.media.codecs.base import StaticSource
import random
import time
import threading

from pyglet.window import key
from pyglet.gl import *
from pyglet import font, shapes, media, resource
from pyglet.media import load, synthesis, SourceGroup
from pyglet.graphics import draw

from .import Board
from pathlib import Path

background = pyglet.graphics.OrderedGroup(0)
window = pyglet.window.Window(485, 600, "tetris")

#font.add_directory((Path(__file__).parent)/"")
#font.add_file("font.ttf")
#k_font = pyglet.font.load("Karmatic Arcade")

sound = pyglet.media.load(str(Path("music.mp3").absolute()), streaming=False)

bg_sound = pyglet.media.Player()


drop_time = 0.7

hold_text = []

board = Board()

def div_vec(vec: tuple[int, ...], scalar: int):
    return *map(lambda x: x // scalar, vec),

def restart_game():
    global board
    
    for block in board.next.blocks:
        block.delete()
    if board.holder:
        for block in board.holder.blocks:
            block.delete()

    board = Board()

class Menu:
    def __init__(self, **options):
        self.current_option = 0
        self._options = options

    @property
    def options(self):
        bg = shapes.BorderedRectangle(
        0, 0, 320, 600, 8,(0,0,0), div_vec((0,0,0),1))
        bg.opacity = 185
        list = [bg]

        text_options = {"font_name": "Source Code pro", "font_size": 18, "color":(255, 255, 255, 255), "anchor_x":'center', "anchor_y":'center', "bold":True}
    
        for index, (option, function) in enumerate(self._options.items()):
            list.append(
                (pyglet.text.Label(("> " + option) if index is self.current_option else option,
                        **text_options,
                        x=160, y= ((265 + (len(self._options) * 35)) - index * 35)
                ))
            )

        return list

    def submit(self):
        list(self._options.values())[self.current_option]()


menu = Menu(resume=board.resume_game, restart=board.init_game,options=board.resume_game)


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
        elif symbol == key.P:
            board.pause_game()
    else:
        if symbol == key.UP:
            menu.current_option = (menu.current_option -1 ) % (len(menu.options) -1)
        elif symbol == key.DOWN:
            menu.current_option = (menu.current_option +1 ) % (len(menu.options) -1)
        elif symbol == key.RETURN:
            menu.submit()

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
        #bg = shapes.BorderedRectangle(
        #60, 100, 200, 400, 8,(200, 200, 200), div_vec((0,0,0),1))
        #bg.opacity = 170

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
                    board.placed_blocks[i[0]][i[1]] = board.current_block.color
                board.spawn_block()
        if(len(board.queue) <= 2):
            board.create_bundle()

    board.update_board()

    pyglet.clock.schedule_once(update_frames, drop_time)

def play_background_sound():
  global bg_sound
  bg_sound.queue(sound)
  bg_sound.volume = 0.04
  bg_sound.play()
  
  # This is optional; it's just a function that keeps the player filled so there aren't any breaks.
  def queue_sounds():
    global bg_sound
    while True:
      bg_sound.queue(sound)
      time.sleep(20) # change this if the background music you have is shorter than 3 minutes
  
  threading.Thread(target=queue_sounds).start()

play_background_sound()

update_frames("")

pyglet.app.run()
