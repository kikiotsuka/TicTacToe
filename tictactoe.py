from __future__ import print_function
import pygame, sys
from pygame.locals import *
from random import randint

class Button:
	def __init__(self, img, loc=(0,0)):
		self.img = img
		self.loc = loc
		self.dim = img.get_size()
		self.box = Rect(loc, self.dim)
	def setloc(self, loc):
		self.loc = loc
		self.box = Rect(loc, self.dim)
	def clicked(self, loc):
		return self.box.collidepoint(loc)

def __main__():
	global board, turn
	pygame.init()
	fpsClock = pygame.time.Clock()

	window = pygame.display.set_mode((500, 600))
	pygame.display.set_caption('Tic Tac Toe')

	#images
	oimg = pygame.image.load('o.png')
	ximg = pygame.image.load('x.png')
	cpubutton = Button(pygame.image.load('cpu.png'))
	cpubutton.setloc((250 - cpubutton.dim[0] / 2, 500 // 3 * 2 - cpubutton.dim[1] / 2))
	twoplayerbutton = Button(pygame.image.load('twoplayer.png'))
	twoplayerbutton.setloc((250 - twoplayerbutton.dim[0] / 2, 
							500 // 3 - twoplayerbutton.dim[1] / 2))
	cpuwin = pygame.image.load('cpuwin.png')
	player1win = pygame.image.load('player1win.png')
	player2win = pygame.image.load('player2win.png')
	draw = pygame.image.load('draw.png')
	replay = Button(pygame.image.load('replay.png'), (0, 0))
	player1turn = pygame.image.load('player1turn.png')
	player2turn = pygame.image.load('player2turn.png')
	cputurn = pygame.image.load('cputurn.png')
	#TODO set replay location

	#clickable tile locations
	tiles = [[0 for x in range(3)] for x in range(3)]
	print(len(tiles))
	i=j=0
	for x in range(0, 500 - 10, 500 // 3):
		for y in range(0, 500 - 10, 500 // 3):
			tiles[i][j] = (Rect(x + 3, y + 3, 500 // 3 - 6, 500 // 3 - 6))
			j += 1
			#print(str(i) + ' ' + str(j))
		i += 1
		j = 0
	turnbox = Rect(0, 500 + 3, 500, 97) #space at bottom = 97 px

	#colors
	RED = pygame.Color(255, 0, 0)
	BLACK = pygame.Color(0, 0, 0)
	WHITE = pygame.Color(255, 255, 255)

	#game states
	menu = True
	playing = False
	gameover = False
	twoplayer = False
	cpu = False

	board = None
	turn = None
	turnboxindicator = []
	turnboxindicator.append(Rect(0, 503, 250, 97))
	turnboxindicator.append(Rect(250, 503, 500, 97))
	while True: #game loop
		window.fill(BLACK)
		if menu:
			window.fill(WHITE)
			window.blit(twoplayerbutton.img, twoplayerbutton.loc)
			window.blit(cpubutton.img, cpubutton.loc)
		elif playing:
			#draw tiles
			for tl in tiles:
				for t in tl:
					pygame.draw.rect(window, WHITE, t)
			pygame.draw.rect(window, WHITE, turnbox)
			if turn:
				pygame.draw.rect(window, RED, turnboxindicator[0])
			else:
				pygame.draw.rect(window, RED, turnboxindicator[1])
			if twoplayer:
				window.blit(player1turn, (5, 508))
				window.blit(player2turn, (500 / 2 + 5, 508))
			elif cpu:
				window.blit(player1turn, (5, 508))
				window.blit(cputurn, (500 / 2 + 5, 508))
		elif gameover:
			pass

		#events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				mouseloc = event.pos
				if menu:
					if twoplayerbutton.clicked(mouseloc):
						menu = False
						twoplayer = True
						playing = True
						board = [[0 for x in range(3)] for x in range(3)]
						turn = True if randint(0, 1) == 0 else False
					elif cpubutton.clicked(mouseloc):
						menu = False
						cpu = True
						playing = True
						turn = True if randint(0, 1) == 0 else False
				elif playing:
					for i, tl in enumerate(tiles):
						for j, t in enumerate(tl):
							if t.collidepoint(mouseloc):
								makemove(i, j)
								print(str(i) + ' ' + str(j))
				else:
					if replay.clicked(mouseloc):
						menu = True
						gameover = False
						cpu = False
						twoplayer = False
		pygame.display.update()
		fpsClock.tick(60)

def makemove(i, j):
	global board, turn
	if board[i][j] == 0:
		if turn:
			board[i][j] = 'x'
		else:
			board[i][j] = 'o'
		turn = not turn
	if checkwin():
		return 1
	if checkdraw():
		return 2
	return 0

def checkwin():
	return horz() or vert() or majdiag() or mindiag()

def horz():
	for bl in board:
		if len(set(bl)) == 1 and 0 not in set(bl):
			return True
	return False

def vert():
	for x in range(0, 3):
		if board[0][x]==board[1][x]==board[2][x]!=0:
			return True
	return False

def majdiag():
	test = []
	for x in range(0, 3):
		test.append(board[x][x])
	return len(set(test)) == 1 and 0 not in set(test)

def mindiag():
	return board[2][0]==board[1][1]==board[0][2]!=0

def checkdraw():
	for bl in board:
		for b in bl:
			if b == 0:
				return False
	return True

__main__()