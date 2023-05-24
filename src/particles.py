import pygame, random


class Particle:
	def __init__(self, pos):
		self.x, self.y = pos[0], pos[1]
		self.vx, self.vy = random.randint(-2,2), random.randint(-2,2)
		self.rad = 5

	def draw(self, win):
		pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.rad)

	def update(self):
		self.x += self.vx
		self.y += self.vy
		if random.randint(0, 100) < 40:
			self.rad -= 1

class Dust:

	def __init__(self, pos):
		self.pos = pos
		self.particles = []
		for i in range(100):
			self.particles.append(Particle(self.pos))

	def update(self):
		for i in self.particles:
			i.update()
			self.particles = [particle for particle in self.particles if particle.rad > 0]

	def draw(self, win):
		for i in self.particles:
			i.draw(win)