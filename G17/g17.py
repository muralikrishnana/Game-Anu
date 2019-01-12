import pygame
from pygame.locals import *
from sys import exit as ex
pygame.init()

screen=pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption("Ball")
BLACK=(0,0,0)

FullScreen = False
x=90
y=60
a=90
b=200

p=708
q=60
r=708
s=200

ny=0
nb=0
nq=0
ns=0

c=400
d=300
nc=1
nd=1

winner="Noone"

firsttime=True
pa=0
pb=0
run=False
play=True

while True:
	for e in pygame.event.get():
		if e.type==QUIT:
			ex()
		if e.type==KEYDOWN :
			if e.key == K_x:
				ex()
			if e.key == K_f:
				FullScreen = not FullScreen
				if FullScreen:
					screen=pygame.display.set_mode((800,600), 0, 32)
				else:
					screen=pygame.display.set_mode((800,600), 0, 32)
				
			if e.key == K_DOWN:
			  	nq=1
				ns=1
			elif e.key == K_UP:
			    if q>=60:
				ns=-1
				nq=-1
			    else:
				nq=0
				ns=0
			elif e.key == K_w:
				ny=-1
				nb=-1
			elif e.key == K_s:
				ny=1
				nb=1
			elif e.key == K_SPACE:
				run = not run
				
		elif e.type==KEYUP:
			if e.key == K_DOWN or K_UP:
				ns=0
				nq=0
			if e.key == K_w or K_s:
				ny=0
				nb=0
	if run:
		c+=nc
		d+=nd
		
	screen.fill((255,255,255))
	if q<60:
		q=60
		nq=0
		s=200
		ns=0
	if s>540:
		s=540
		ns=0
		q=400
		nq=0
	if y<60:
		y=60
		ny=0
		b=200
		nb=0
	if b>540:
		b=540
		nb=0
		ny=0
		y=400
	if c<(x+10) and y<=d and b>=d:
		c=x+10
		nc=-1*nc
	if c>(p-10) and q<=d and s>=d:
		c=p-10
		nc=-1*nc
	if c>740:
		c=740
		nc=-1*nc
		pa+=1
	if c<60:
		c=60
		nc=-1*nc
		pb+=1
	if d>530:
		d=530
		nd=-1*nd
	if d<60:
		d=60
		nd=-1*nd
		
	if pa>=10 or pb>=10:
		BLACK = (105,105,105)
		if firsttime:
			if pa==10: 
				winner = "Player A"
			elif pb==10: winner = "Player B"
			firsttime = not firsttime
			c-=1
			d-=1
			run = not run
		my_font1 = pygame.font.SysFont("ubuntu", 40)
		win=my_font1.render(winner+" wins the game", True, (0,0,0))
		screen.blit(win, (210,250))
		if e.type == KEYDOWN:
			if e.key == K_n:

				x=90
				y=60
				a=90
				b=200

				p=708
				q=60
				r=708
				s=200

				ny=0
				nb=0	
				nq=0
				ns=0

				c=400
				d=300


				winner="Noone"

				firsttime=True
				pa=0
				pb=0
				run=False
				BLACK=(0,0,0)
		screen.blit(my_font.render("Press N for new game", True, (0,0,0)), (325,300))

	q+=nq
	s+=ns
	y+=ny
	b+=nb
	pygame.draw.rect(screen, BLACK,(50,50,700,500), 5)
	pygame.draw.line(screen, BLACK, (x,y),(a,b), 10)
	pygame.draw.line(screen, BLACK, (p,q),(r,s),10)
	pygame.draw.circle(screen, BLACK, (c,d), 10)

	my_font = pygame.font.SysFont("arial", 16)
	sa = my_font.render("Player A - {}".format(pa), True, (0,0,0))
	sb = my_font.render("Player B - {}".format(pb), True, (0,0,0))
	det=my_font.render("Press X to exit               Press SPACEBAR to pause", True, (0,0,0))
	screen.blit(sa, (50,20))
	screen.blit(sb, (670,20))
	screen.blit(det, (50,570))

	
	
	pygame.display.update()
