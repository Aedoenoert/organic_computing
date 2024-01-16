from tkinter import Frame, Label, CENTER
import random
import logic
import constants as c

def gen(grid_len):
    return random.randint(0, grid_len - 1)

class GameGrid(Frame):
    def __init__(self, grid_len):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_down)
        self.grid_len = grid_len

        self.commands = {
            c.KEY_UP: logic.up,
            c.KEY_DOWN: logic.down,
            c.KEY_LEFT: logic.left,
            c.KEY_RIGHT: logic.right,
            c.KEY_UP_ALT1: logic.up,
            c.KEY_DOWN_ALT1: logic.down,
            c.KEY_LEFT_ALT1: logic.left,
            c.KEY_RIGHT_ALT1: logic.right,
            c.KEY_UP_ALT2: logic.up,
            c.KEY_DOWN_ALT2: logic.down,
            c.KEY_LEFT_ALT2: logic.left,
            c.KEY_RIGHT_ALT2: logic.right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = logic.new_game(self.grid_len)
        self.history_matrixs = []
        self.update_grid_cells()

        #self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(self.grid_len):
            grid_row = []
            for j in range(self.grid_len):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / self.grid_len,
                    height=c.SIZE / self.grid_len
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=c.GRID_PADDING,
                    pady=c.GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(self.grid_len):
            for j in range(self.grid_len):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="",bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = event
        #print(event)
        if key == c.KEY_QUIT: exit()
        #if key == c.KEY_BACK and len(self.history_matrixs) > 1:
        #    self.matrix = self.history_matrixs.pop()
        #    self.update_grid_cells()
        #    print('back on step total step:', len(self.history_matrixs))
        if key in self.commands:
            self.matrix, done = self.commands[key](self.matrix, self.grid_len)
            if done:
                self.matrix = logic.add_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                if logic.game_state(self.matrix) == 'win':
                    self.grid_cells[0][0].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[0][1].configure(text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if logic.game_state(self.matrix) == 'lose':
                    self.grid_cells[0][0].configure(text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[0][1].configure(text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (gen(self.grid_len), gen(self.grid_len))
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(self.grid_len), gen(self.grid_len))
        self.matrix[index[0]][index[1]] = 2
