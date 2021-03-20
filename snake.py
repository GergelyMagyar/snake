import pygame
import random
import time
import collections
from collections import namedtuple


screen_width = 800
screen_height = 600
cell_size = 20


cell_count_w = screen_width//cell_size
cell_count_h = screen_height//cell_size

Dimensions = namedtuple("Dimensions", "sw sh cs ccw cch")
dimensions = Dimensions(screen_width, screen_height, cell_size, cell_count_w, cell_count_h)

pygame.init()

random.seed(time.localtime())
clock = pygame.time.Clock()

pygame.display.set_caption("Snake")

win = pygame.display.set_mode((screen_width, screen_height))


class Rectangle(object):
	def __init__(self, x, y, i, j, dimensions, win):
		self.x = x
		self.y = y
		self.i = i
		self.j = j
		self.screen_dim = dimensions
		self.win = win

	def draw(self, color):
		pygame.draw.rect(self.win, color, (self.x, self.y, self.screen_dim.cs, self.screen_dim.cs))


class Grid(object):
	def __init__(self, dimensions, win, background_color = (0,0,0)):
		self.board = []
		self.screen_dim = dimensions
		self.win = win
		self.background_color = background_color

		row = []
		x = 0
		y = 0
		for j in range(self.screen_dim.cch):
			row.clear()
			x = 0
			for i in range(self.screen_dim.ccw):
				row.append(Rectangle(x,y,i,j,self.screen_dim,self.win))
				x += self.screen_dim.cs
			self.board.append(row[:])
			y += self.screen_dim.cs

		self.draw()

	def draw(self, color = None):
		for row in self.board:
			for rect in row:
				if(color == None):
					rect.draw(self.background_color)
				else:
					rect.draw(color)


class Snake(object):
	def __init__(self, spawn_i, spawn_j, dimensions, win, board, color=(124,252,0)):
		self.body = []
		self.body.insert(0, board[spawn_j][spawn_i])
		self.length = 1
		self.screen_dim = dimensions
		self.win = win
		self.board = board
		self.color = color
		self.direction = random.randint(0,4) # 0 - up, 1 - down, 2 - left, 3 - right

	def move(self):
		
		newi = self.body[0].i
		newj = self.body[0].j
		if self.direction == 0: 	# UP
			newj -= 1
			if newj < 0:
				return False
		elif self.direction == 1: 	# DOWN
			newj += 1
			if newj > self.screen_dim.cch-1:
				return False
		elif self.direction == 2: 	# LEFT
			newi -= 1
			if newi < 0:
				return False
		else: 						# RIGHT
			newi += 1
			if newi > self.screen_dim.ccw-1:
				return False

		self.body.insert(0, self.board[newj][newi])

		# if no fruit
		self.body.pop()

		return True


	def draw(self):
		for rect in self.body:
			rect.draw(self.color)


def redraw(dimensions, win, grid, snake):
	#win.fill((0,0,0))
	grid.draw()
	snake.draw()
	pygame.display.update()





def solo_game(dimensions, win, clock):
	pygame.mouse.set_visible(False)
	grid = Grid(dimensions, win, (0,0,0))
	snake = Snake(10, 10, dimensions, win, grid.board, (124,252,0))
	redraw(dimensions, win, grid, snake)

	run = True
	while(run):
		clock.tick(20)
		pygame.time.delay(100)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] or keys[pygame.K_UP]:
			snake.direction = 0
		if keys[pygame.K_s] or keys[pygame.K_DOWN]:
			snake.direction = 1
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			snake.direction = 2
		if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
			snake.direction = 3

		run = snake.move()
		redraw(dimensions, win, grid, snake)


solo_game(dimensions, win, clock)
