import puzzle as pz
import constants as c
import logic as log


def move(direction):  # CONTROL
    if direction == "up":
        c.current_game.key_down(c.KEY_UP)
    elif direction == "right":
        c.current_game.key_down(c.KEY_RIGHT)
    elif direction == "down":
        c.current_game.key_down(c.KEY_DOWN)
    elif direction == "left":
        c.current_game.key_down(c.KEY_LEFT)


def reset(grid_len):  # CONTROL
    if c.current_game is not None:
        c.current_game.destroy()
    c.current_game = pz.GameGrid(grid_len)
    c.points = 0
    pass


def state():  # OBSERVE
    game_state = log.game_state(c.current_game.matrix)
    end = False
    if game_state != 'not over':
        end = True
    return c.current_game.matrix, c.points, end
