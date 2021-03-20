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
	def __init__(self, x, y, dimensions, win):
		self.x = x
		self.y = y
		self.screen_dim = dimensions
		self.win = win

	def draw(self, color):
		pygame.draw.rect(self.win, color, (self.x, self.y, self.screen_dim.sw, self.screen_dim.sh))


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
				row.append(Rectangle(x,y,self.screen_dim,self.win))
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

def redraw(dimensions, win, grid):
	#win.fill((0,0,0))
	grid.draw()
	pygame.display.update()







def solo_game(dimensions, win, clock):
	pygame.mouse.set_visible(False)
	grid = Grid(dimensions, win, (0,0,0))
	redraw(dimensions, win, grid)

	run = True
	while(run):
		clock.tick(20)
		pygame.time.delay(100)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False


solo_game(dimensions, win, clock)
