import pygame
import requests


class GetSudoku:
    def __init__(self, size, level):
        self.url = f"http://www.cs.utep.edu/cheon/ws/sudoku/new/?size={size}&level={level}"
        self.board = [[-1 for _ in range(9)] for __ in range(9)]
        self.prefilled = [[0 for ___ in range(9)] for ____ in range(9)]

    def getBoard(self):
        try:
            response = requests.get(self.url)
            if response.json()['response']:
                for i in response.json()['squares']:
                    x, y, value = i['x'], i['y'], i['value']
                    self.board[y][x] = value
                    self.prefilled[y][x] = 1
                return self.board, self.prefilled
            else:
                return f"Error: {response.json()['reason']}", None
        except:
            return "Check Internet Connection", None


class Solver:
    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == -1:
                    return (i, j)  # row, col
        return None

    def valid(self, board, num, pos):
        # Check row
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False
        # Check column
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False
        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False
        return True

    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i
                if self.solve(board):
                    return True
                board[row][col] = -1
        return False


class Main:
    def __init__(self):
        pygame.init()
        self.board, self.prefilled, self.solution, self.temp_board, self.temp_prefilled = None, None, None, None, None
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((600, 650))
        self.running = True
        self.frame_count = 0
        self.frame_rate = 10
        pygame.display.set_caption("Sudoku")
        pygame.display.set_icon(pygame.image.load("./images/icon.jpg"))
        self.pale_yellow = (255, 253, 204)
        self.white = (255, 255, 255)
        self.yellow = (255, 247, 48)
        self.black = (0, 0, 0)
        self.border_lines = self.getBorderLine()
        self.middle_lines = self.getMinddleLine()
        self.center = self.getCenter()
        self.grid = self.getGrid()
        self.level = 1
        self.active = [1, 0, 0]
        self.cell_selected = [0 for _ in range(81)]
        self.run_timer = False
        self.paused = False
        self.generate_pressed, self.confirm_generate = False, True
        self.clear_pressed, self.confirm_clear = False, False
        self.solution_pressed, self.confirm_solution = False, False
        self.display = False
        self.win = False
        self.not_filled = False
        self.lose = False
        self.co = 0
        self.error_mat = None
        self.pause = pygame.image.load("./images/pause.png")
        self.pause = pygame.transform.scale(self.pause, (35, 35))
        self.play = pygame.image.load("./images/play.png")
        self.play = pygame.transform.scale(self.play, (35, 35))
        self.clear = pygame.image.load("./images/images.png")
        self.clear = pygame.transform.scale(self.clear, (30, 30))
        self.erase = pygame.image.load("./images/erase.png")
        self.erase = pygame.transform.scale(self.erase, (30, 30))

    def getBorderLine(self):
        return [((75, 150), (525, 150)), ((75, 150), (75, 600)), ((75, 600), (525, 600)), ((525, 150), (525, 600)),
                ((75, 300), (525, 300)), ((75, 450), (525, 450)), ((225, 150), (225, 600)), ((375, 150), (375, 600))]

    def getMinddleLine(self):
        return [((75, 200), (525, 200)), ((75, 250), (525, 250)), ((75, 350), (525, 350)), ((75, 400), (525, 400)),
                ((75, 500), (525, 500)), ((75, 550), (525, 550)), ((
                    125, 150), (125, 600)), ((175, 150), (175, 600)),
                ((275, 150), (275, 600)), ((325, 150), (325, 600)), ((425, 150), (425, 600)), ((475, 150), (475, 600))]

    def getCenter(self):
        return [[(100, 175), (150, 175), (200, 175), (250, 175), (300, 175), (350, 175), (400, 175), (450, 175), (500, 175)],
                [(100, 225), (150, 225), (200, 225), (250, 225), (300,
                                                                  225), (350, 225), (400, 225), (450, 225), (500, 225)],
                [(100, 275), (150, 275), (200, 275), (250, 275), (300,
                                                                  275), (350, 275), (400, 275), (450, 275), (500, 275)],
                [(100, 325), (150, 325), (200, 325), (250, 325), (300,
                                                                  325), (350, 325), (400, 325), (450, 325), (500, 325)],
                [(100, 375), (150, 375), (200, 375), (250, 375), (300,
                                                                  375), (350, 375), (400, 375), (450, 375), (500, 375)],
                [(100, 425), (150, 425), (200, 425), (250, 425), (300,
                                                                  425), (350, 425), (400, 425), (450, 425), (500, 425)],
                [(100, 475), (150, 475), (200, 475), (250, 475), (300,
                                                                  475), (350, 475), (400, 475), (450, 475), (500, 475)],
                [(100, 525), (150, 525), (200, 525), (250, 525), (300,
                                                                  525), (350, 525), (400, 525), (450, 525), (500, 525)],
                [(100, 575), (150, 575), (200, 575), (250, 575), (300, 575), (350, 575), (400, 575), (450, 575), (500, 575)]]

    def getGrid(self):
        return [[0 for i in range(9)] for j in range(9)]

    def addText(self, msg, color):
        font = pygame.font.SysFont(None, 25)
        text = font.render(msg, True, color)
        text_rect = text.get_rect()
        text_rect.center = 300, 625
        self.screen.blit(text, text_rect)

    def buttonText(self, msg, x, y):
        gen = pygame.font.SysFont(None, 30).render(msg, True, "Black")
        gen_rec = gen.get_rect()
        gen_rec.center = x, y
        self.screen.blit(gen, gen_rec)

    def getErroredMatrix(self, board, solution):
        error_mat = [[0 for __ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j] != solution[i][j]:
                    error_mat[i][j] = 1
        return error_mat

    def addTextFont25(self, msg, color, pos):
        font = pygame.font.SysFont(None, 25)
        text = font.render(msg, True, color)
        self.screen.blit(text, pos)

    def addTextFont35(self, msg, color, pos):
        font = pygame.font.SysFont(None, 35)
        text = font.render(msg, True, color)
        self.screen.blit(text, pos)

    def addTextFont45(self, msg, color, center):
        font = pygame.font.SysFont(None, 45)
        text = font.render(msg, True, color)
        text_rect = text.get_rect()
        text_rect.center = center
        self.screen.blit(text, text_rect)

    def drawButton(self, color, pos, msg, x, y):
        pygame.draw.rect(self.screen, color, pos)
        self.buttonText(msg, x, y)

    def alterGrid(self, s1=0, e1=0, s2=0, e2=0):
        for i in range(s1, e1):
            for j in range(s2, e2):
                self.grid[i][j] = 1

    def changeActive(self, ind):
        self.active = [0 for i in range(3)]
        self.active[ind] = 1
        self.level = ind + 1

    def startGame(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            key_pressed = pygame.key.get_pressed()
            self.drawButton((122, 160, 255), [
                            75, 20, 145, 60], "Generate", 147.5, 50)
            self.drawButton((125, 250, 148), [
                            230, 20, 145, 60], "Check", 302.5, 50)
            self.drawButton((135, 255, 251), [
                            385, 20, 145, 60], "Solution", 457.5, 50)
            total_seconds = self.frame_count // self.frame_rate
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            output_string = "{0:02}:{1:02}".format(minutes, seconds)
            self.addTextFont35(output_string, self.black, [450, 105])
            self.addTextFont25("Level", self.black, [75, 90])
            for i in range(len(self.active)):
                if self.active[i] == 1:
                    pygame.draw.circle(self.screen, (125, 250, 148),
                                       (100 + (50 * i), 125), 15)
                else:
                    pygame.draw.circle(self.screen, (0, 0, 0),
                                       (100 + (50 * i), 125), 15, 2)
            self.addTextFont25("E", self.black, [95, 117])
            self.addTextFont25("M", self.black, [143, 117])
            self.addTextFont25("H", self.black, [193, 117])
            self.screen.blit(self.clear, (270, 100))
            if not self.paused:
                self.screen.blit(self.pause, (320, 100))
            else:
                self.screen.blit(self.play, (320, 100))
            self.screen.blit(self.erase, (370, 103))
            for row in range(9):
                for column in range(9):
                    color = self.white
                    if self.grid[row][column] == 1:
                        color = self.pale_yellow
                    if self.grid[row][column] == 2:
                        color = self.yellow
                    pygame.draw.rect(self.screen, color, [
                        75 + (column * 50), 150 + (row * 50), 50, 50])
            for j in self.middle_lines:
                pygame.draw.line(self.screen, (0, 0, 255), j[0], j[1], 1)
            for i in self.border_lines:
                pygame.draw.line(self.screen, (0, 0, 0), i[0], i[1], 2)
            if self.board and not self.paused and self.prefilled:
                for i in range(9):
                    for j in range(9):
                        if self.board[i][j] != -1:
                            t_color = "Black"
                            if self.prefilled[i][j] != 1:
                                t_color = "Blue"
                            if self.error_mat:
                                if self.error_mat[i][j] == 1 and self.prefilled[i][j] != 1:
                                    t_color = "Red"
                            self.addTextFont45(
                                str(self.board[i][j]), t_color, self.center[i][j])
            if key_pressed[pygame.K_q]:
                self.running = False
            if not self.board or self.display:
                self.addText("Press Generate to start the game", "Green")
            if type(self.board) != list:
                self.addText(self.board, "Red")
            else:
                if self.paused and not self.generate_pressed:
                    self.addText("Game Paused", "Red")
                if self.solution_pressed:
                    self.addText(
                        "You want to quit and see solution? Space / Esc", "Red")
                    if key_pressed[pygame.K_SPACE]:
                        self.confirm_solution, self.solution_pressed = True, False
                    if key_pressed[pygame.K_ESCAPE]:
                        self.confirm_solution, self.solution_pressed = False, False
                if self.board:
                    if self.generate_pressed:
                        self.paused, self.display, self.run_timer = True, False, False
                        self.addText(
                            "Space To Confirm, ESC To continue", "Red")
                        if key_pressed[pygame.K_SPACE]:
                            self.confirm_generate, self.paused, self.run_timer, self.generate_pressed, self.solution_pressed = True, False, True, False, False
                        if key_pressed[pygame.K_ESCAPE]:
                            self.confirm_generate, self.paused, self.run_timer, self.generate_pressed = False, False, True, False
                if self.confirm_solution:
                    self.board = self.solution
                    self.prefilled = [
                        [1 for i in range(9)] for j in range(9)]
                    self.run_timer = False
                    self.confirm_solution = False
                    self.solution_pressed = False
                    self.display = True
                if self.clear_pressed and self.board:
                    self.addText(
                        "Space to clear all input / ESC to continue", "Red")
                    if key_pressed[pygame.K_SPACE]:
                        self.confirm_clear = True
                        self.clear_pressed = False
                    if key_pressed[pygame.K_ESCAPE]:
                        self.confirm_clear = False
                        self.clear_pressed = False
                if self.confirm_clear:
                    self.board = [x[:] for x in self.temp_board]
                    self.prefilled = [x[:] for x in self.temp_prefilled]
                    self.confirm_clear = False
                if self.confirm_generate:
                    genBoard = GetSudoku(9, self.level)
                    self.board, self.prefilled = genBoard.getBoard()
                    if type(self.board) == list:
                        self.solution = [x[:] for x in self.board]
                        self.temp_board = [x[:] for x in self.board]
                        self.temp_prefilled = [x[:] for x in self.prefilled]
                        Solver().solve(self.solution)
                        self.run_timer = True
                        self.frame_count = 0
                        self.confirm_generate = False
                if self.not_filled:
                    self.addText("All cells are Not Filled", "Yellow")
                if self.win and not self.display:
                    self.addText(
                        "Solved!! You Won. Click Generate to start new", "Green")
                    self.run_timer = False
                if self.lose:
                    self.error_mat = self.getErroredMatrix(
                        self.board, self.solution)
                    self.addText("Errors!! Not Solved", "Red")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        self.not_filled, self.lose = False, False
                        x, y = pygame.mouse.get_pos()
                        if x not in range(370, 401) and y not in range(100, 130):
                            cell_selected = [0 for _ in range(81)]
                        self.grid = self.getGrid()
                        # Top Buttons
                        if y in range(20, 81):
                            # generate button
                            if x in range(75, 221):
                                self.win = False
                                if self.board:
                                    self.generate_pressed = True
                                if self.confirm_generate:
                                    genBoard = GetSudoku(9, self.level)
                                    self.board, self.prefilled = genBoard.getBoard()
                                    if type(self.board) == list:
                                        self.solution = [x[:]
                                                         for x in self.board]
                                        self.temp_board = [x[:]
                                                           for x in self.board]
                                        self.temp_prefilled = [x[:]
                                                               for x in self.prefilled]
                                        Solver().solve(self.solution)
                                        self.run_timer = True
                                        self.frame_count = 0
                                        self.confirm_generate = False
                            # check button
                            if x in range(230, 376):
                                if self.board:
                                    self.check_board = [
                                        _ for s in self.board for _ in s]
                                    if self.check_board.count(-1) == 0:
                                        if self.board == self.solution:
                                            self.win = True
                                        else:
                                            self.lose = True
                                    else:
                                        self.not_filled = True
                            # solution button
                            if x in range(385, 531):
                                if self.board:
                                    self.solution_pressed = True
                        # Tool Buttons
                        if y in range(100, 130) and self.board:
                            # Clear Button
                            if x in range(270, 301):
                                if self.board and not self.win:
                                    self.clear_pressed = True
                            # Pause Button
                            if x in range(320, 351) and not self.win:
                                if self.board:
                                    self.run_timer = not self.run_timer
                                    self.paused = not self.paused
                            if x in range(370, 401) and not self.win:
                                if any(self.cell_selected):
                                    x_ind, y_ind = self.cell_selected.index(
                                        1) // 9, self.cell_selected.index(1) % 9
                                    if self.prefilled[x_ind][y_ind] != 1:
                                        self.board[x_ind][y_ind] = -1
                        # Select Level
                        if y in range(110, 141):
                            if x in range(85, 116):
                                self.changeActive(0)
                            if x in range(135, 166):
                                self.changeActive(1)
                            if x in range(185, 216):
                                self.changeActive(2)
                        # Select and color cells
                        if(x > 74 and x < 526 and y > 149 and y < 601):
                            self.error_mat = None
                            self.cell_selected = [0 for _ in range(81)]
                            y = (y - 150) // 50
                            x = (x - 75) // 50
                            for i in range(9):
                                self.grid[y][i] = 1
                                self.grid[i][x] = 1
                            if(y in range(3)):
                                if(x in range(3)):
                                    self.alterGrid(0, 3, 0, 3)
                                if(x in range(3, 6)):
                                    self.alterGrid(0, 3, 3, 6)
                                if(x in range(6, 9)):
                                    self.alterGrid(0, 3, 6, 9)
                            if(y in range(3, 6)):
                                if(x in range(3)):
                                    self.alterGrid(3, 6, 0, 3)
                                if(x in range(3, 6)):
                                    self.alterGrid(3, 6, 3, 6)
                                if(x in range(6, 9)):
                                    self.alterGrid(3, 6, 6, 9)
                            if(y in range(6, 9)):
                                if(x in range(3)):
                                    self.alterGrid(6, 9, 0, 3)
                                if(x in range(3, 6)):
                                    self.alterGrid(6, 9, 3, 6)
                                if(x in range(6, 9)):
                                    self.alterGrid(6, 9, 6, 9)
                            self.grid[y][x] = 2
                            if self.board:
                                self.cell_selected[y * 9 + x] = 1
            if any(self.cell_selected):
                cell_x, cell_y = self.cell_selected.index(
                    1) // 9, self.cell_selected.index(1) % 9
                if self.prefilled[cell_x][cell_y] != 1:
                    if key_pressed[pygame.K_1] or key_pressed[pygame.K_KP1]:
                        self.board[cell_x][cell_y] = 1
                    if key_pressed[pygame.K_2] or key_pressed[pygame.K_KP2]:
                        self.board[cell_x][cell_y] = 2
                    if key_pressed[pygame.K_3] or key_pressed[pygame.K_KP3]:
                        self.board[cell_x][cell_y] = 3
                    if key_pressed[pygame.K_4] or key_pressed[pygame.K_KP4]:
                        self.board[cell_x][cell_y] = 4
                    if key_pressed[pygame.K_5] or key_pressed[pygame.K_KP5]:
                        self.board[cell_x][cell_y] = 5
                    if key_pressed[pygame.K_6] or key_pressed[pygame.K_KP6]:
                        self.board[cell_x][cell_y] = 6
                    if key_pressed[pygame.K_7] or key_pressed[pygame.K_KP7]:
                        self.board[cell_x][cell_y] = 7
                    if key_pressed[pygame.K_8] or key_pressed[pygame.K_KP8]:
                        self.board[cell_x][cell_y] = 8
                    if key_pressed[pygame.K_9] or key_pressed[pygame.K_KP9]:
                        self.board[cell_x][cell_y] = 9
            if self.board and self.run_timer:
                self.frame_count += 1
            if self.co == 0 and self.board:
                for i in range(9):
                    for j in range(9):
                        print(self.solution[i][j], end=" ")
                    print()
                self.co += 1
            self.clock.tick(self.frame_rate)
            pygame.display.update()
        pygame.quit()


Main().startGame()
