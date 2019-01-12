import os
import sys
if getattr(sys, 'frozen', False):
	top_folder = sys._MEIPASS
else :
	top_folder = 'files'
# Lib import
import pygame
import math
import random
import time
from pygame.locals import *

# Initializing The Game
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Toy Farm")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('files/pics/anim_1.png'), (32, 32)))

screen_width, screen_height= 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

# Loading Images
screen_background = pygame.image.load('files/pics/canvas_background.jpg')
screen_background = pygame.transform.scale(screen_background, (screen_width+133, screen_height+50))
cloud_1 = pygame.transform.scale(pygame.image.load('files/pics/cloud_1.png'), (160, 75))
cloud_2 = pygame.transform.scale(pygame.image.load('files/pics/cloud_2.png'), (180, 75))
cloud_3 = pygame.transform.scale(pygame.image.load('files/pics/cloud_3.png'), (155, 75))
cloud_4 = pygame.transform.scale(pygame.image.load('files/pics/cloud_4.png'), (180, 75))
cloud_5 = pygame.transform.scale(pygame.image.load('files/pics/cloud_5.png'), (180, 75))
tank_width, tank_height = 150, 160
tank = pygame.transform.scale(pygame.image.load('files/pics/tank.png'), (tank_width, tank_height))
mis_width, mis_height = 15, 60
missile = pygame.transform.scale(pygame.image.load('files/pics/missile.png'), (mis_width, mis_height))
raindrop = pygame.transform.scale(pygame.image.load('files/pics/raindrop.png'), (8, 15))
alien0 = pygame.transform.scale(pygame.image.load('files/pics/alien_1.png'), (30, 40))
alien2 = pygame.transform.scale(pygame.image.load('files/pics/alien_2.png'), (30, 50))
alien3 = pygame.transform.scale(pygame.image.load('files/pics/alien_3.png'), (26, 50))
blasting = pygame.transform.scale(pygame.image.load('files/pics/blast.png'), (30, 36))
al = [alien0, alien2, alien3]
alien1 = al[random.randint(0,2)]
health_bar = pygame.image.load('files/pics/farm_health_bar.png')
health_green = pygame.image.load('files/pics/health.png')
squirrel = pygame.transform.scale(pygame.image.load('files/pics/anim_3.png'), (220,220))
elephant = pygame.transform.scale(pygame.image.load('files/pics/elephant.png'), (200,260))
cow = pygame.transform.scale(pygame.image.load('files/pics/anim_1.png'), (200,215))
smilie = pygame.transform.scale(pygame.image.load('files/pics/smilie.png'), (200,200))
dog = pygame.transform.scale(pygame.image.load('files/pics/dog.png'), (220,260))
won_e = pygame.transform.scale(pygame.image.load('files/pics/won_e.png'), (240,250))
health_low = False
start_time = 0
game_won, game_lost = False, False
aliens_hit = 0

#sound
collide = pygame.mixer.Sound("files/sound/collide.wav")
collide.set_volume(0.05)
shoot = pygame.mixer.Sound("files/sound/shoot.wav")
shoot.set_volume(0.05)
alien_hit = pygame.mixer.Sound("files/sound/blast.wav")
alien_hit.set_volume(0.1)
rain_music = pygame.mixer.Sound("files/sound/rain.wav")
rain_music.set_volume(0.05)

#BGM
pygame.mixer.music.load('files/sound/peace.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

game_running = 0

# Cloud Movement
duty_cloud = []
duty_cloud_x = []
duty_cloud_y = []
cloud_onduty = 0
fps = [0, 0, 0, 0, 0]

#Keys and Clouds
cloud = [cloud_1, cloud_2, cloud_3, cloud_4, cloud_5]
keys = [False, False]
tank_pos = [500-(tank_width/2), 610]
acc = [0, 0]
missiles = []

rain = []
rain_pos = random.randint(100, 600)
rain_cloud_x, rain_cloud_y = random.randint(950, 1000), random.randint(200, 270)
rain_time = 0
rain_cloud_speed = 0
no_rain = True
rain_fall = -5
raindrops = []
k = 0
b_index = 0
b_blast = True
health_farm = 194
time_start = 0

#aliens
alien_timer = 100
alien_timer1 = 0
aliens = [[100, -100]]
fan_pos = [-32, 305]
fan_r = 150*math.sqrt(2)
fan_dx = 1/(math.sqrt(8)*math.pi)

# Main loop
intro = 1
intro_1 = 1
intro_2 = 0
intro_3 = 0
intro_4 = 0
running=1
while running:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			if event.key == K_x:
				exit()


	#Choosing Cloud(s) in View
	while cloud_onduty < 5:
		index = random.randint(0,4)
		duty_cloud.append(cloud[index])
		duty_cloud_x.append(random.randint(950, 1000))
		duty_cloud_y.append(random.randint(180, 260))
		cloud_onduty += 1

	screen.blit(screen_background, (-68,0))

	#RAIN
	screen.blit(cloud_4, (rain_cloud_x, rain_cloud_y))
	if no_rain :	
		rain_cloud_speed += 1
		if rain_cloud_speed == 2:
			rain_cloud_speed = 0
			rain_cloud_x -= 1
	#Rain Starts
	if rain_cloud_x == rain_pos:
		no_rain = False
		rain_time += 1
		rain_music.play()
		for i in range(10, 170, 20):
			raindrops.append([rain_pos+i, rain_cloud_y+50])
			drop_append = False
		for drop in raindrops:	
			index = 0
			drop[1] += 20
			if drop[1] >= 650:
				raindrops.pop(index)
				index+=1
			screen.blit(raindrop, (drop[0], drop[1]+rain_fall))
			rain_fall *= -1

		if rain_time == 600:
			rain_time = 0
			no_rain = True
			rain_music.stop()



	if rain_cloud_x < -500:
		rain_pos = random.randint(50, 600)
		rain_cloud_x, rain_cloud_y = random.randint(950, 1000), random.randint(200, 270)
		rain_time = 0
		rain_cloud_speed = 0
		no_rain = True
		rain_fall = -5
		raindrops = []

	#RAIN_Complete

	#Displaying Cloud(s) in View
	for i in range(0, cloud_onduty):
		screen.blit(duty_cloud[i], (duty_cloud_x[i], duty_cloud_y[i]))
		
		fps[i] += 1
		if fps[i] == 5:
			fps[i] = 0
			duty_cloud_x[i] -= i+1

		if duty_cloud_x[i] < -220:
			duty_cloud_x.pop(i)
			duty_cloud_y.pop(i)
			duty_cloud.pop(i)
			cloud_onduty -= 2

	#Game Active Check
	if game_running:
		if time_start == True:
			time_start = False
			start_time = pygame.time.get_ticks()
		mouse_pos = pygame.mouse.get_pos()
		y = tank_pos[1]
		x = tank_pos[0]
		if tank_pos[0]>710:
			tank_pos[0] = 710
		if tank_pos[0]<90:
			tank_pos[0] = 90
		angle = math.atan2(mouse_pos[1]-y, mouse_pos[0]-x)
		rotated_tank = pygame.transform.rotate(tank, 270-(180/math.pi)*angle)
		tank_new_pos = (tank_pos[0]-rotated_tank.get_rect().width/2, tank_pos[1]-rotated_tank.get_rect().height/2)
		screen.blit(rotated_tank, tank_new_pos)
		
		for mis in missiles:
			index = 0
			velx = 10*math.cos(mis[0])
			vely = 10*math.sin(mis[0])
			mis[1] += velx
			mis[2] += vely
			if mis[1] < -100 or mis[1] > 900 or mis[2] < -100 or mis[2] > 700:
				missiles.pop(index)
			index += 1
			for projectile in missiles:
				new_missile = pygame.transform.rotate(missile, 270-(180/math.pi)*projectile[0])
				screen.blit(new_missile, (projectile[1], projectile[2]))

		#alien
		if alien_timer == 0:
			aliens.append([random.randint(50, 750), -200])
			alien_timer = 100 - (alien_timer1*2)
			if alien_timer1>35:
				alien_timer = 35
			else:
				alien_timer1+=1
		index = 0
		for alien in aliens:
			if alien[1] > 480:
				blast = alien
				for i in range (0, 3000):
					screen.blit(blasting, (blast[0], blast[1]))
				aliens.pop(index)

			alien[1] += 1
			if (pygame.time.get_ticks()-time_start) > 30000:
				alien[1] += 1
			elif (pygame.time.get_ticks()-time_start) > 10000:
				alien[1] += 2
			if alien[1] == 480 or alien[1] == 481:
				health_low = True
       			alien_rect = pygame.Rect(alien1.get_rect())
       			alien_rect.top = alien[1]
        		alien_rect.left = alien[0]
        		if alien_rect.top > 480:
            			alien_hit.play()
				aliens_hit += 1
            			aliens.pop(index)
			#Check for blasts
			index1=0
        		for misile in missiles:
            			bullrect = pygame.Rect(missile.get_rect())
            			bullrect.left = misile[1]
            			bullrect.top = misile[2]
            			if alien_rect.colliderect(bullrect):
                			collide.play()
                			acc[0]+=1
                			aliens.pop(index)
                			missiles.pop(index1)

            		index1+=1
			index +=1
		for alien in aliens:
			screen.blit(alien1, alien)
		alien_timer -= 0.5
		#/alien
		#Score
		font = pygame.font.Font(None, 25)
		game_timer = font.render("Time Remaining : "+str((60000-(int(pygame.time.get_ticks())-start_time))/60000)+":"+str((60000-(int(pygame.time.get_ticks())-start_time))/1000%60).zfill(2), True, (0,0,0))
		time_display = game_timer.get_rect()
		time_display.topright = [780, 14]
		screen.blit(game_timer, time_display)

		#Health
		screen.blit(health_bar, (11,11))
		if health_low:
			health_low = False
			health_farm -= 20
		for i in range(0, health_farm):
			screen.blit(health_green, ((i+14),14))
		if (pygame.time.get_ticks()-start_time) >= 60000:
			game_running = False
			running = False
			game_won = True
		if health_farm <= 0:
			game_running = False
			running = False
			game_lost = True
		if game_won:
			accuracy = (((float(acc[0])-aliens_hit)*100)/acc[1])
		else:
			accuracy = 0

		#Get Input
		for e in pygame.event.get():
			if e.type == QUIT:
				exit()
			if e.type == KEYDOWN :
				if e.key == K_RIGHT:
					keys[0] = True
				elif e.key == K_LEFT:
					keys[1] = True
			if e.type == KEYUP :
				if e.key == K_RIGHT:
					keys[0] = False
				elif e.key == K_LEFT:
					keys[1] = False
			if e.type == MOUSEBUTTONDOWN :
				shoot.play()
				mouse_pos = pygame.mouse.get_pos()
				y = tank_pos[1]
				x = tank_pos[0]
				angle = math.atan2(mouse_pos[1]-y, mouse_pos[0]-x)
				missiles.append([math.atan2(mouse_pos[1]-y, mouse_pos[0]-x), tank_new_pos[0]+tank_width/2, tank_new_pos[1]
+tank_height/2])
				acc[1] += 1
		if keys[0]:
			tank_pos[0] += 5
		elif keys[1]:
			tank_pos[0] -= 5

	if intro:
		if intro_1:
			input_font = pygame.font.Font(None, 17)
			intro_font = pygame.font.Font(None, 30)
			intro_text_1 = intro_font.render("Hi Chief!!!", True, (255,255,255))
			intro_text_2 = intro_font.render("Welcome to Toy Farm!!!", True, (255,255,255))
			intro_text_3 = intro_font.render("Wow plesant weather!!!", True, (255,255,255))
			pygame.draw.rect(screen, (139, 69, 19), (270, 80, 400, 150))
			pygame.draw.rect(screen, (255, 255, 255), (275, 85, 390, 140), 3)
			screen.blit(intro_text_1, (368, 110))
			screen.blit(intro_text_2, (368, 130))
			screen.blit(intro_text_3, (368, 160))
			screen.blit(input_font.render("Press ENTER to Proceed>>", True, (255,255,255)), (468, 190))
			screen.blit(squirrel, (120, 50))
			for ev in pygame.event.get():
				if ev.type == KEYDOWN:
					if ev.key == K_RETURN:
						intro_1 = 0
						intro_2 = 1
				if ev.type == QUIT:
					exit()
		if intro_2:
			input_font = pygame.font.Font(None, 17)
			intro_font = pygame.font.Font(None, 30)
			intro_text_1 = intro_font.render("Oh No!! Chief... Somebody is", True, (255,255,255))
			intro_text_2 = intro_font.render("attacking our Toy Farm!!!", True, (255,255,255))
			pygame.draw.rect(screen, (218, 165, 32), (270, 80, 400, 150))
			pygame.draw.rect(screen, (255, 255, 255), (275, 85, 390, 140), 3)
			screen.blit(intro_text_1, (333, 130))
			screen.blit(intro_text_2, (333, 150))
			screen.blit(input_font.render("Press ENTER to Proceed>>", True, (255,255,255)), (468, 190))
			screen.blit(smilie, (120, 60))
			for ev in pygame.event.get():
				if ev.type == KEYDOWN:
					if ev.key == K_RETURN:
						intro_2 = 0
						intro_3 = 1
				if ev.type == QUIT:
					exit()
		if intro_3:
			input_font = pygame.font.Font(None, 17)
			intro_font = pygame.font.Font(None, 30)
			intro_text_1 = intro_font.render("Don't Worry Chief... We have a", True, (255,255,255))
			intro_text_2 = intro_font.render("TANK to defend the missiles!!", True, (255,255,255))
			pygame.draw.rect(screen, (128, 128, 128), (270, 80, 400, 150))
			pygame.draw.rect(screen, (255, 255, 255), (275, 85, 390, 140), 3)
			screen.blit(intro_text_1, (333, 130))
			screen.blit(intro_text_2, (333, 150))
			screen.blit(input_font.render("Press ENTER to Proceed>>", True, (255,255,255)), (468, 190))
			screen.blit(elephant, (140, 20))
			for ev in pygame.event.get():
				if ev.type == KEYDOWN:
					if ev.key == K_RETURN:
						intro_3 = 0
						intro_4 = 4
				if ev.type == QUIT:
					exit()
		if intro_4:
			input_font = pygame.font.Font(None, 17)
			intro_font = pygame.font.Font(None, 25)
			intro_text_1 = intro_font.render("Use Left, Right arrow keys to", True, (255,255,255))
			intro_text_2 = intro_font.render("control the TANK. Use mouse to ", True, (255,255,255))
			intro_text_3 = intro_font.render("aim and Press mouse button to Shoot..", True, (255,255,255))
			intro_text_4 = intro_font.render("Please SAVE OUR TOY FARM, CHIEF", True, (255,255,255))
			pygame.draw.rect(screen, (219, 122, 147), (270, 80, 400, 150))
			pygame.draw.rect(screen, (255, 255, 255), (275, 85, 390, 140), 3)
			screen.blit(intro_text_1, (323, 105))
			screen.blit(intro_text_2, (323, 125))
			screen.blit(intro_text_3, (323, 145))
			screen.blit(intro_text_4, (323, 165))
			screen.blit(input_font.render("Press ENTER to Start the Game>>", True, (255,255,255)), (468, 190))
			screen.blit(cow, (142, 38))
			for ev in pygame.event.get():
				if ev.type == KEYDOWN:
					if ev.key == K_RETURN:
						intro_4 = 0
						game_running = True
						time_start = True
				if ev.type == QUIT:
					exit()
	pygame.display.flip()

#Results Display
if game_won : 
	pygame.font.init()
	score = pygame.font.Font(None, 35)
	score_text = score.render("Score is : "+str(int(accuracy)), True, (255,255,255))
	score_value = score_text.get_rect()
	score_value.centerx = screen.get_rect().centerx+100
	score_value.centery = 145
	lost_text = pygame.font.Font(None, 25)
	won_text = pygame.font.Font(None, 25)
	won = pygame.font.Font(None, 40)
	results = won_text.render("TOTAL SHOTS : "+str(acc[1])+"  TOTAL HITS : "+str(acc[0]), True, (255, 255, 255))
	results_view = results.get_rect()
	results_view.centerx = screen.get_rect().centerx+100
	results_view.centery = 180
	pygame.draw.rect(screen, (0, 255, 0), (180, 50, 580, 200))
	pygame.draw.rect(screen, (255, 255, 255), (185, 55, 570, 190), 2)
	win = won.render("Voila!!! Our Toy Farm is safe!!!", True, (255, 255, 255))
	win_view = win.get_rect()
	win_view.centerx = screen.get_rect().centerx+100
	win_view.centery = 110
	screen.blit(win, win_view)
	screen.blit(score_text, score_value)
	screen.blit(results, results_view)
	screen.blit(won_e, (50, 12))
	pygame.display.flip()
else:
	pygame.font.init()
	score = pygame.font.Font(None, 35)
	score_text = score.render("Score is : "+str(int(accuracy)), True, (255,255,255))
	score_value = score_text.get_rect()
	score_value.centerx = screen.get_rect().centerx+100
	score_value.centery = 145
	lost_text = pygame.font.Font(None, 25)
	lost = pygame.font.Font(None, 40)
	results = lost_text.render("TOTAL SHOTS : "+str(acc[1])+"  TOTAL HITS : "+str(acc[0]), True, (255, 255, 255))
	results_view = results.get_rect()
	results_view.centerx = screen.get_rect().centerx+100
	results_view.centery = 180
	pygame.draw.rect(screen, (255, 0, 0), (180, 50, 580, 200))
	pygame.draw.rect(screen, (255, 255, 255), (185, 55, 570, 190), 2)
	lost = lost.render("Ohh!! Toy Farm is Destroyed!!", True, (255, 255, 255))
	lost_view = lost.get_rect()
	lost_view.centerx = screen.get_rect().centerx+100
	lost_view.centery = 110
	screen.blit(lost, lost_view)
	screen.blit(results, results_view)
	screen.blit(score_text, score_value)
	screen.blit(dog, (90, 25))
	pygame.display.flip()
while True:
	for e in pygame.event.get():
		if e.type == QUIT:
			exit()
	
