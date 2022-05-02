"""The game of tetris, using pyglet. """

import numpy as np
import pyglet as pg

window = pg.window.Window(resizable=True, caption="Tetris (not)")

crate = pg.resource.image("images/crate.png")
empty = pg.resource.image("images/turd.png")
# crate.anchor_x = crate.width//2
# crate.anchor_y = crate.height//2

game_title = pg.text.Label("Tetris (not)", font_name='Times New Roman', font_size=36,
                           x=window.width/2, y = window.height * 0.95, anchor_x = 'center', anchor_y = 'center')

import pyglet.graphics as graphics
import pyglet.gl as gl
import random


class gameboard:
    def __init__(self):
        self.size = 10
        self.board = []
        for i in range(self.size):
            self.board.append([0 for i in range(self.size)])
        self.active_piece = None
        self.width = window.width * 0.8
        self.height = window.height * 0.8
        self.iconsize = window.width / 15

        self.spawn_piece()

    def render_board(self):
        for i in range(self.size):
            for j in range(self.size):
                x, y = self.arr_to_screen((i, j))
                if self.board[j][i] > 0:
                    crate.blit(x, y, width=self.iconsize, height=self.iconsize)
                else:
                    empty.blit(x, y, width=self.iconsize, height=self.iconsize)

    def arr_to_screen(self, loc):
        x = loc[0]
        y = loc[1]
        return ((x + 1) / self.size) * self.width, ((self.size - y - 1) / self.size) * self.height

    def update(self):
        [print(self.board[i]) for i in range(self.size)]
        print(self.active_piece.locations)
        print("")

        for row_ind in range(self.size):
            # if exists a row below and that row is empty, fall
            if row_ind+1 < self.size and sum(self.board[row_ind+1]) == 0:
                self.board[row_ind+1] = self.board[row_ind]
                self.board[row_ind] = [0 for i in range(self.size)]
            # if the row is complete, empty it
            if sum(self.board[row_ind]) == self.size:
                self.board[row_ind] = [0 for i in range(self.size)]

        moved = self.move_down()
        if not moved:
            self.spawn_piece()


    def spawn_piece(self):
        x = np.random.choice(range(self.size - 1))
        piece = tetris_piece([(x,0), (x+1, 0)])

        for location in piece.locations:
            self.board[location[1]][location[0]] = 1
        self.active_piece = piece

    def can_move(self, direction, x, y):
        if direction == 'down':
            return y + 1 < self.size and self.board[y+1][x] == 0
        elif direction == 'left':
            return x - 1 >= 0 and self.board[y][x-1] == 0
        elif direction == 'right':
            return x + 1 < self.size and self.board[y][x+1] == 0
        else:
            return False

    def move_left(self):
        locations = self.active_piece.locations
        can_move = True
        for loc in locations:
            can_move = can_move and self.can_move('left', loc[0], loc[1])
        if can_move:
            for loc in locations:
                self.board[loc[1]][loc[0]] = 0
                print('set', loc, 'to zero')
            self.active_piece.locations = [(loc[0]-1, loc[1]) for loc in locations]
            for loc in self.active_piece.locations:
                self.board[loc[1]][loc[0]] = 1
                print('set', loc, 'to one')

        return can_move

    def move_right(self):
        locations = self.active_piece.locations
        can_move = True
        for loc in locations:
            can_move = can_move and self.can_move('right', loc[0], loc[1])
        if can_move:
            for loc in locations:
                self.board[loc[1]][loc[0]] = 0
                print('set', loc, 'to zero')
            self.active_piece.locations = [(loc[0]+1, loc[1]) for loc in locations]
            for loc in self.active_piece.locations:
                self.board[loc[1]][loc[0]] = 1
                print('set', loc, 'to one')

        return can_move

    def move_down(self):
        locations = self.active_piece.locations
        can_move = True
        for loc in locations:
            can_move = can_move and self.can_move('down', loc[0], loc[1])
        if can_move:
            for loc in locations:
                self.board[loc[1]][loc[0]] = 0
                print('set', loc, 'to zero')
            self.active_piece.locations = [(loc[0], loc[1]+1) for loc in locations]
            for loc in self.active_piece.locations:
                self.board[loc[1]][loc[0]] = 1
                print('set', loc, 'to one')

        return can_move



class tetris_piece:
    def __init__(self, locations):
        self.locations = locations


board = gameboard()


@window.event
def on_draw():
    window.clear()
    game_title.draw()
    board.render_board()
    board.update()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pg.window.key.A or symbol == pg.window.key.LEFT:
        print('A')
        board.move_left()
    elif symbol == pg.window.key.D or symbol == pg.window.key.RIGHT:
        print('D')
        board.move_right()
    elif symbol == pg.window.key.R or symbol == pg.window.key.SPACE:
        print('R')


#pg.clock.schedule_interval(on_draw, 1/2)
pg.app.run()
    # pg.app.EventLoop().sleep(0.5)
    # window.dispatch_event('on_draw')
