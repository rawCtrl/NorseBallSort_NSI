import pygame
from pygame import *
import random
import time
import traceback
from Tube import * 
from Ball import *

class Main:
	def __init__(self):
		pygame.init()
		pygame.font.init()
		self.police64 = pygame.font.Font("font.ttf", 64)
		self.police2 = pygame.font.Font("font1.ttf", 54)
		self.fenetre = pygame.display.set_mode((800,600))
		pygame.display.set_caption("NorseBallSort")
		self.fenetre.fill((11,28,58))
		self.etat = True
		self.plateau = []
		self.balls = []
		self.action = 0
		self.ball = None
		
		for ii in ["rouge", "bleu", "jaune"]:
			self.balls += [(pygame.image.load(f"img/{ii}.png").convert_alpha(),pygame.image.load(f"img/{ii}1.png").convert_alpha().get_rect(), ii)]

		self.tube = pygame.image.load("img/Tube2.png").convert_alpha()
		self.tube_rect = self.tube.get_rect()
		self.tube_rect = self.tube_rect.move(175, 200)

		for _ in range(5):
			self.plateau += [Tube(self.tube_rect)]
			self.tube_rect = self.tube_rect.move(100, 0)

		for i in self.balls:
			for _ in range(4):
				x = random.randint(0, 2)
				while len(self.plateau[x].pile) >= 4:
					x = random.randint(0, 2)
				self.plateau[x].pile += [Ball(i[1].move(182 + x * 100, 365 - 50 * len(self.plateau[x].pile)), i[2], i[0])]	

	def dessiner(self):
		self.fenetre.fill((11,28,58))
		for i in self.plateau:
			self.fenetre.blit(self.tube, i.rect)
			for j in i.pile:
				self.fenetre.blit(j.img, j.rect) 
		
		if self.ball != None:
			self.fenetre.blit(self.ball.img, self.ball.rect)

	def gagner(self):
		for i in self.plateau:
			if i.est_gagne() == False:
				return False
		return True

	def ecran_victoire(self, temps):
		img_vic = pygame.image.load(f"img/fond{random.randint(0,3)}.jpg").convert_alpha()
		img_vic = pygame.transform.scale(img_vic, (800, 600))
		img_vic_rect = img_vic.get_rect()
		self.fenetre.fill((189,134,51))
		self.fenetre.blit(img_vic, img_vic_rect)
		self.fenetre.blit(self.police2.render(f"Vous avez réussi en {temps} secondes", True, (255,255,0)), (68, 200))
		self.fenetre.blit(self.police2.render(f"Cliquez pour quitter", True, (255,255,0)), (218, 300))
		pygame.display.flip()
		
		while True:
			for i in pygame.event.get():
				if i.type == MOUSEBUTTONDOWN or i.type == QUIT:
					return False

	def jeu(self):
		pygame.mixer.music.load(f"musique/musique{random.randint(5, 5)}.wav")
		temps_debut = time.time()
		#pygame.mixer.music.play()
		continuer = 1

		while continuer == 1:
			temps = round(time.time() - temps_debut, 2)
			temp_texte = self.police64.render(str(temps), True, (139,132,123))
			
			if self.gagner() == True:
				continuer = 0

			#self.fenetre.fill((11,28,58))
			self.dessiner()
			self.fenetre.blit(temp_texte, (348, 28))
			
			pygame.display.flip()

			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN:
					if self.etat:
						for i in range(len(self.plateau)):
							for b in range(len(self.plateau[i].pile)):
								if self.plateau[i].rect.collidepoint(event.pos) == True and self.plateau[i].pile != [] and self.action == 0:
									self.ball = self.plateau[i].pile.pop(-1)
									self.ball.rect.update(382, 122, 40, 40)
									self.dessiner()
									self.fenetre.blit(temp_texte, (348, 28))
									pygame.display.flip()
									self.action += 1
									self.etat = False
									break				

					else:
						for j in range(len(self.plateau)):
							if self.plateau[j].rect.collidepoint(event.pos) == True and self.plateau[j].peut_empiler(self.ball) == True and self.action == 0:
								self.plateau[j].empiler(self.ball)
								print(self.plateau[j].peut_empiler(self.ball))
								self.plateau[j].pile[-1].rect.update(182 + j * 100, 415 - 50 * len(self.plateau[j].pile), 40, 40)
								self.ball = None
								self.action += 1
								self.etat = True
								self.dessiner()
								self.fenetre.blit(temp_texte, (348, 28))
								pygame.display.flip()

				elif event.type == QUIT:
					return False

				self.action = 0 

		self.ecran_victoire(temps)
		
main = Main()
main.dessiner()
pygame.display.flip()
main.jeu()
pygame.mixer.music.unload()	
pygame.font.quit()				
pygame.quit()
exit()
