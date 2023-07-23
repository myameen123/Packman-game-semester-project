from bounds import random_poss
import tkinter as tk
from constants import *


class GenerateFood():
	def __init__(self, window, pac, imgs, count):
		self.window = window
		self.pac = pac
		self.img = imgs[0]
		self.bonus_img = imgs[1]
		self.count = count

		# CREATING FOOD ITEMS
		pac_x, pac_y = float(self.pac.place_info()['x']), float(self.pac.place_info()['y'])
		foods = []
		for i in range(count):
			food_x, food_y = random_poss(object='food')
			while abs(food_x-pac_x) < 64 or abs(food_y-pac_y) < 36:
				food_x, food_y = random_poss(object='food')
			food = tk.Label(window, image=self.img, bd=0)
			food.place(x=food_x, y=food_y)
			foods.append(food)
		self.foods = foods


	def eaten(self):
		pac_x, pac_y = float(self.pac.place_info()['x']), float(self.pac.place_info()['y'])
		for food in self.foods:
			food_x, food_y = float(food.place_info()['x']), float(food.place_info()['y'])
			dy = food_x - pac_x
			dx = food_y - pac_y
			if dy < 18 and dy > -12 and dx < 22 and dx > -13:
				return food

	def change_food(self, eaten_food):
		pac_x, pac_y = float(self.pac.place_info()['x']), float(self.pac.place_info()['y'])
		food_x, food_y = random_poss(object='food')
		if abs(food_x-pac_x) < 200 or abs(food_y-pac_y) < 100:
			self.change_food(eaten_food)
		else:
			eaten_food.place(x=food_x, y=food_y)