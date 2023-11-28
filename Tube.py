from Ball import *

class Tube:
	def __init__(self, rect):
		self.rect = rect
		self.pile = []

	def peut_empiler(self, c):
		if self.pile != []:
			if self.pile[-1].couleur != c.couleur or len(self.pile) >= 4:
				return False
		return True

	def empiler(self, c: Ball):
		self.pile += [c]

	def depiler(self):
		return self.pile.pop(-1)

	def est_gagne(self):
		if len(self.pile) == 4 or self.pile == []:
			for i in self.pile:
				if self.pile[0].couleur != i.couleur:
					return False
			return True
		return False
		 