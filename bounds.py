import random
from constants import pac_size, food_size, ghost_size, maze_img_url

# FETCHING THE RECTANGLES AND CORNERS OF THE MAZE
with open('mapping.txt', 'r') as f:
	file = f.read()
	file_rect, file_corners, file_centre_rects = file.split('\n')

	lines = file_rect.split(";")[:-1]
	rects = []
	for line in lines:
		rect = []
		for number in line.split(','):
			rect.append(int(number))
		rects.append(rect)

	lines = file_corners.split(";")[:-1]
	corners = []
	for line in lines:
		corner = []
		for number in line.split(','):
			corner.append(int(number))
		corners.append(corner)

	lines = file_centre_rects.split(";")[:-1]
	cent_rects = []
	for line in lines:
		cent_rect = []
		for number in line.split(','):
			cent_rect.append(int(number))
		cent_rects.append(cent_rect)

if maze_img_url == "Static/maze_simple.png":
	for centre_rect in cent_rects:
		rects.remove(centre_rect)

def outOfBound(cords, object='pac'):
	x, y = cords
	if object == 'pac':
		x2, y2 = x + pac_size[0], y + pac_size[1]
	elif object == 'food':
		x2, y2 = x + food_size[0], y + food_size[1]
	elif object == 'ghost':
		x2, y2 = x + ghost_size[0], y + ghost_size[1]
	x_mid = (x + x2) / 2
	y_mid = (y + y2) / 2
	for r in rects:
		if r[0] <= x and r[1] <= y and r[2] >= x and r[3] >= y:
			return True
		elif r[0] <= x2 and r[1] <= y2 and r[2] >= x2 and r[3] >= y2:
			return True
		elif r[0] <= x2 and r[1] <= y and r[2] >= x2 and r[3] >= y:
			return True
		elif r[0] <= x and r[1] <= y2 and r[2] >= x and r[3] >= y2:
			return True
		elif r[0] <= x_mid and r[1] <= y_mid and r[2] >= x_mid and r[3] >= y_mid:
			return True
	return False

def random_poss(object):
	x = random.randrange(0, 800)
	y = random.randrange(0, 600)
	if not outOfBound((x, y), object=object):
		return x, y
	else:
		return random_poss(object=object)