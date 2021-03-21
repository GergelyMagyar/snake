import pygame
import random
import time
import collections
from collections import namedtuple
from tkinter import *

pygame.init()

screen_width = 800
screen_height = 600
cell_size = 20


cell_count_w = screen_width//cell_size
cell_count_h = screen_height//cell_size

Dimensions = namedtuple("Dimensions", "sw sh cs ccw cch")
dimensions = Dimensions(screen_width, screen_height, cell_size, cell_count_w, cell_count_h)

bigfont = pygame.font.SysFont('Comic Sans MS', 80)
smallfont = pygame.font.SysFont('Comic Sans MS', 30)
fonts = (bigfont, smallfont)

random.seed(time.localtime())
clock = pygame.time.Clock()

pygame.display.set_caption("Snake")

win = pygame.display.set_mode((screen_width, screen_height))


class Rectangle(object):
	def __init__(self, x, y, i, j, dimensions, win, rectangle_type="background"):
		self.type = rectangle_type
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
				row.append(Rectangle(x,y,i,j,self.screen_dim,self.win,"background"))
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
	def __init__(self, spawn_i, spawn_j, dimensions, win, board, fruit, color=(124,252,0)):
		self.body = []
		self.body.insert(0, board[spawn_j][spawn_i])
		self.length = 1
		self.screen_dim = dimensions
		self.win = win
		self.board = board
		self.fruit = fruit
		self.color = color
		self.direction = random.randint(0,3) # 0 - up, 1 - down, 2 - left, 3 - right

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

		if self.body[0].type == "fruit":
			self.fruit.spawn()
		elif self.body[0].type == "snake":
			return False
		else:
			self.body.pop().type = "background"

		self.body[0].type = "snake"

		return True

	def draw(self):
		for rect in self.body:
			rect.draw(self.color)


class Fruit(object):
	def __init__(self, dimensions, win, board, color=(255,0,0)):
		self.dimensions = dimensions
		self.win = win
		self.board = board
		self.color = color
		self.rect = None
		self.spawn()

	def spawn(self):
		random_i = random.randint(0, self.dimensions.ccw-1)
		random_j = random.randint(0, self.dimensions.cch-1)

		while self.board[random_j][random_i].type != "background":
			random_i = random.randint(0, self.dimensions.ccw-1)
			random_j = random.randint(0, self.dimensions.cch-1)

		self.rect = self.board[random_j][random_i]
		self.rect.type = "fruit"

	def draw(self):
		if self.rect != None:
			self.rect.draw(self.color)


def redraw(dimensions, win, grid, fruit, snake):
	#win.fill((0,0,0))
	grid.draw()
	fruit.draw()
	snake.draw()
	pygame.display.update()


def solo_game(dimensions, win, clock, fonts):
	pygame.mouse.set_visible(False)
	grid = Grid(dimensions, win, (0,0,0))
	fruit = Fruit(dimensions, win, grid.board, color=(255,0,0))
	snake = Snake(10, 10, dimensions, win, grid.board, fruit, (124,252,0))
	redraw(dimensions, win, grid, fruit, snake)

	run = True
	while(run):
		clock.tick(20)
		pygame.time.delay(100)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if (keys[pygame.K_w] or keys[pygame.K_UP]) and snake.direction != 1:
			snake.direction = 0
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and snake.direction != 0:
			snake.direction = 1
		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and snake.direction != 3:
			snake.direction = 2
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and snake.direction != 2:
			snake.direction = 3

		run = snake.move()
		redraw(dimensions, win, grid, fruit, snake)


def ai_game(dimensions, win, clock, fonts):
	pass


def center_text(w,h, tw, th):
	x = w//2-tw//2
	y = h//2 - th//2
	return x,y


def draw_menu(dimensions, win, fonts):
	win.fill((0,0,0))

	title = fonts[0].render("Snake", True, (255,255,255))
	x, y = center_text(dimensions.sw, dimensions.sh, title.get_width(), title.get_height())
	win.blit(title, (x,y))

	solo = fonts[1].render("<- Solo Game", True, (255,255,255))
	x, y = center_text(dimensions.sw, dimensions.sh, solo.get_width(), solo.get_height())
	x -= dimensions.sw//3
	win.blit(solo, (x,y))

	ai = fonts[1].render("AI Game ->", True, (255,255,255))
	x, y = center_text(dimensions.sw, dimensions.sh, ai.get_width(), ai.get_height())
	x += dimensions.sw//3
	win.blit(ai, (x,y))

	exit = fonts[1].render("v exit v", True, (255,255,255))
	x, y = center_text(dimensions.sw, dimensions.sh, exit.get_width(), exit.get_height())
	y += dimensions.sh//3 + exit.get_height()
	win.blit(exit, (x,y))

	pygame.display.update()


def menu(dimensions, win, clock, fonts):
	run = True
	while(run):
		draw_menu(dimensions, win, fonts)

		clock.tick(20)
		pygame.time.delay(100)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			solo_game(dimensions, win, clock, fonts)
		if keys[pygame.K_RIGHT]:
			ai_game(dimensions, win, clock, fonts)
		if keys[pygame.K_DOWN]:
			run = False



menu(dimensions, win, clock, fonts)
