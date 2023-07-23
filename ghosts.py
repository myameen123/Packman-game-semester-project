import tkinter as tk
import random
from bounds import *
from constants import *

class Ghost():
	def __init__(self, window, pac, ghost_imgs):
		self.window = window
		self.pac = pac
		self.orig_imgs = ghost_imgs
		self.imgs = ghost_imgs[2:]
		self.ghosts = []
		self.speeds = []
		self.movement_types = []
		self.dirs = []
		self.atCorner = []
		self.count = 0
		self.img_count = len(ghost_imgs)
		self.movements = [
			{'x': 0, 'y': -1},   # up
			{'x': 0, 'y': 1},    # down
			{'x': 1, 'y': 0},    # right
			{'x': -1, 'y': 0},   # left
		]

	def create_ghost(self, speed, movement_type):
		if len(self.imgs) == 0:
			self.imgs = self.orig_imgs[2:]
		if movement_type == 'follow':
			selected_img = self.orig_imgs[0]
		elif movement_type == 'ambush':
			selected_img = self.orig_imgs[1]
		else:
			selected_img = random.choice(self.imgs)
			self.imgs.remove(selected_img)
		ghost = tk.Label(self.window, image=selected_img, bd=0)
		ghost_x, ghost_y = random_poss(object='ghost')
		ghost.place(x=ghost_x, y=ghost_y)
		self.count += 1
		self.ghosts.append(ghost)
		self.dirs.append(random.choice(self.movements))
		self.speeds.append(speed)
		self.movement_types.append(movement_type)
		self.atCorner.append(False)

	def move_ghosts(self, pac_dir):
		for i in range(self.count):

			ghost_x, ghost_y = float(self.ghosts[i].place_info()['x']), float(self.ghosts[i].place_info()['y'])
			pac_x, pac_y = float(self.pac.place_info()['x']), float(self.pac.place_info()['y'])

			if ghost_x <= -24 or ghost_x >= 777:
				ghost_x = 777 - abs(ghost_x)

			if self.movement_types[i] == 'random':
	
				# IF IT HITS A CORNER
				if not self.atCorner[i]:
					ghost_x_mid = ghost_x + ghost_size[0]/2
					ghost_y_mid = ghost_y + ghost_size[1]/2
					for corner in corners:
						corner_x, corner_y = corner
						dx = abs(corner_x - ghost_x_mid)
						dy = abs(corner_y - ghost_y_mid)
						if (dx <= 5 or dy <= 5) and dx < 30 and dy < 30:
							self.atCorner[i] = True
							self.dirs[i] = random.choice(self.movements)


				ghost_x += self.speeds[i] * self.dirs[i]['x']
				ghost_y += self.speeds[i] * self.dirs[i]['y']

				# IF IT HITS THE WALL
				while outOfBound((ghost_x, ghost_y), object='ghost'):
					ghost_x -= self.speeds[i] * self.dirs[i]['x']
					ghost_y -= self.speeds[i] * self.dirs[i]['y']
					self.dirs[i] = random.choice(self.movements)
					ghost_x += self.speeds[i] * self.dirs[i]['x']
					ghost_y += self.speeds[i] * self.dirs[i]['y']
					self.atCorner[i] = False

			elif self.movement_types[i] == 'follow' or self.movement_types[i] == 'ambush':
				new_dirs = self.movements[:]
				new_dirs.remove({'x': -self.dirs[i]['x'], 'y': -self.dirs[i]['y']})

				dirs = []
				ds = []
				for dir in new_dirs:
					step_x = ghost_x + self.speeds[i] * dir['x']
					step_y = ghost_y + self.speeds[i] * dir['y']

					if not outOfBound((step_x, step_y), object='ghost'):

						if self.movement_types[i] == 'follow':
							target_x, target_y = pac_x, pac_y
						elif self.movement_types[i] == 'ambush':
							target_x = pac_x + pac_dir['x']*ambush_distance
							target_y = pac_y + pac_dir['y']*ambush_distance

						d = (target_x - step_x) ** 2 + (target_y - step_y) ** 2
						dirs.append(dir)
						ds.append(d)

				if len(set(ds)) == len(ds):
					try:
						d_min = min(ds)
					except:
						self.dirs[i] = {'x': -self.dirs[i]['x'], 'y': -self.dirs[i]['y']}
						ghost_x += self.speeds[i] * self.dirs[i]['x']
						ghost_y += self.speeds[i] * self.dirs[i]['y']
						self.ghosts[i].place(x=ghost_x, y=ghost_y)
						continue
						
					self.dirs[i] = dirs[ds.index(d_min)]
				else:
					d_max = max(ds)
					i_to_remove = ds.index(d_max)
					ds.pop(i_to_remove)
					dirs.pop(i_to_remove)

					if {'x': 0, 'y': -1} in dirs:
						self.dirs[i] = {'x': 0, 'y': -1}
					elif {'x': -1, 'y': 0} in dirs:
						self.dirs[i] = {'x': -1, 'y': 0}
					elif {'x': 0, 'y': 1} in dirs:
						self.dirs[i] = {'x': 0, 'y': 1}
					else:
						self.dirs[i] = {'x': 1, 'y': 0}

				ghost_x = ghost_x + self.speeds[i] * self.dirs[i]['x']
				ghost_y = ghost_y + self.speeds[i] * self.dirs[i]['y']

			if ghost_x <= -24 or ghost_x >= 800:
				ghost_x = 800 - abs(ghost_x)

			self.ghosts[i].place(x=ghost_x, y=ghost_y)




	def check_collision(self):
		pac_x, pac_y = float(self.pac.place_info()['x']), float(self.pac.place_info()['y'])
		for ghost in self.ghosts:
			ghost_x, ghost_y = float(ghost.place_info()['x']), float(ghost.place_info()['y'])
			dx, dy = ghost_x - pac_x, ghost_y - pac_y
			if dx < 23 and dx > -19 and dy < 21 and dy > -21:
				return True
		return False

	def recreate(self, initial_n_of_ghosts=2):
		for ghost in self.ghosts:
			ghost.destroy()
		starting_ghosts_speeds = self.speeds[:initial_n_of_ghosts]
		starting_ghosts_movement_types = self.movement_types[:initial_n_of_ghosts]
		self.__init__(self.window, self.pac, self.orig_imgs)
		for i in range(initial_n_of_ghosts):
			self.create_ghost(starting_ghosts_speeds[i], starting_ghosts_movement_types[i])