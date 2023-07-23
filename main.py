'''
Created by:
1) Armaghan
2) Muhammad Yameen
3) Hassan Fakhar
'''


import tkinter as tk
import time
from bounds import outOfBound, random_poss
from food import *
from ghosts import Ghost
from constants import *
from bar import get_bar
from copy import copy
from tkinter import messagebox

# CREATING WINDOW
root = tk.Tk()
root.title('P A C M A N')
root.geometry(f"850x600+0+0")
def main_loop():
	global dir, pac, stopped, user_keys,stopped, score, highscore, pac_x, pac_y, level, user_keys, ghosts_stopped, affected, speed, times_touched, orig_variables
	main_canvas.place_forget()
	stopped = True
	ghosts_stopped = False
	affected = True
	score = 0
	highscore = variables['highscore']
	dir = {'x':0, 'y':0}
	user_keys = ''
	orig_speed = speed
	orig_variables = copy(variables)

	times_touched = 0

	maze_img = tk.PhotoImage(file=maze_img_url)
	game_over_img = tk.PhotoImage(file='static/gameover_img.png')
	pac_img_R = tk.PhotoImage(file=pac_R_url)
	pac_img_L = tk.PhotoImage(file=pac_L_url)
	pac_img_U = tk.PhotoImage(file=pac_U_url)
	pac_img_D = tk.PhotoImage(file=pac_D_url)
	pac_img_eaten = tk.PhotoImage(file=pac_eaten_url)
	food_img = tk.PhotoImage(file=food_url)
	food_colored_img = tk.PhotoImage(file=food_colored_url)
	play_img = tk.PhotoImage(file=play_url)
	pause_img = tk.PhotoImage(file=pause_url)
	instruction_img = tk.PhotoImage(file=instruction_url)
	boss_img = tk.PhotoImage(file=boss_url)
	black_img = tk.PhotoImage(file=black_url)

	blue_img = tk.PhotoImage(file=blue_url)
	pink_img = tk.PhotoImage(file=pink_url)
	red_img = tk.PhotoImage(file=red_url)
	sky_img = tk.PhotoImage(file=sky_url)
	yellow_img = tk.PhotoImage(file=yellow_url)
	brown_img = tk.PhotoImage(file=brown_url)
	green_img = tk.PhotoImage(file=green_url)
	ghost_imgs = [red_img, sky_img, pink_img, blue_img, yellow_img, brown_img, green_img]



	# HANDLING KEYS
	def pressed(event):
		global dir, pac, stopped, user_keys
		user_keys += event.keysym

		if event.keysym == "Right":
			stopped = False
			tog.configure(image=pause_img)
			dir['x'] = 1
			dir['y'] = 0
			pac.configure(image=pac_img_R)
		elif event.keysym == "Left":
			stopped = False
			tog.configure(image=pause_img)
			dir['x'] = -1
			dir['y'] = 0
			pac.configure(image=pac_img_L)
		elif event.keysym == "Up":
			stopped = False
			tog.configure(image=pause_img)
			dir['x'] = 0
			dir['y'] = -1
			pac.configure(image=pac_img_U)
		elif event.keysym == "Down":
			stopped = False
			tog.configure(image=pause_img)
			dir['x'] = 0
			dir['y'] = 1
			pac.configure(image=pac_img_D)
		elif event.keysym == "space":
			stopped = True
			tog.configure(image=play_img)
			dir['x'] = 0
			dir['y'] = 0
	root.bind_all("<Key>", pressed)


	# CREATING MAZE
	tk.Label(
		root,
		image=maze_img,
		bd=0,
	).place(x=0, y=0)

	# CREATE PACMAN
	pac = tk.Label(root, image=pac_img_R, bd=0)
	pac_x, pac_y = random_poss(object='pac')
	pac.place(x=pac_x, y=pac_y)


	# CREATE FOOD
	foods = GenerateFood(root, pac, [food_img, food_colored_img], food_count)

	# GET GHOSTS
	my_ghost = Ghost(window=root, ghost_imgs=ghost_imgs, pac=pac)
	my_ghost.create_ghost(speed=speed_follower, movement_type='follow')
	my_ghost.create_ghost(speed=speed_ambush, movement_type='ambush')
	for i in range(initial_n_of_ghosts-2):
		my_ghost.create_ghost(speed=speed_ghost, movement_type='random')


	# SETTING THE GAME ENGINE
	def gameEngine():
		global stopped, score, highscore, pac_x, pac_y, level, user_keys, ghosts_stopped, affected, speed, times_touched, orig_variables

		# SETTING BOSS KEYS
		if 'easy' in user_keys.lower():
			my_ghost.speeds[my_ghost.movement_types.index('ambush')] = speed_follower - level_speed_increment
			my_ghost.speeds[my_ghost.movement_types.index('follow')] = speed_ambush - level_speed_increment
			variables['difficulty'] = "easy"
			user_keys = ''
		elif 'medium' in user_keys.lower():
			my_ghost.speeds[my_ghost.movement_types.index('ambush')] = speed_follower
			my_ghost.speeds[my_ghost.movement_types.index('follow')] = speed_ambush
			variables['difficulty'] = "medium"
			user_keys = ''
		elif 'hard' in user_keys.lower():
			my_ghost.speeds[my_ghost.movement_types.index('ambush')] = speed_follower + level_speed_increment
			my_ghost.speeds[my_ghost.movement_types.index('follow')] = speed_ambush + level_speed_increment
			variables['difficulty'] = "hard"
			user_keys = ''
		elif 'clip' in user_keys.lower():
			if ghosts_stopped:
				ghosts_stopped = False
			else:
				ghosts_stopped = True
			user_keys = ''
		elif 'affected' in user_keys.lower():
			if affected:
				affected = False
			else:
				affected = True
			user_keys = ''
		elif 'faster' in user_keys.lower():
			speed += speed_increment
			user_keys = ''
		elif 'slower' in user_keys.lower():
			speed -= speed_increment
			user_keys = ''
		elif 'default' in user_keys.lower():
			speed = orig_speed
			ghosts_stopped = False
			my_ghost.speeds[my_ghost.movement_types.index('ambush')] = speed_follower
			my_ghost.speeds[my_ghost.movement_types.index('follow')] = speed_ambush
			variables['difficulty'] = "medium"
			user_keys = ''
		elif 'changemap' in user_keys.lower():
			if variables['maze_img_url'] == "Static/maze_simple.png":
				variables['maze_img_url'] = "Static/maze.png"
			else:
				variables['maze_img_url'] = "Static/maze_simple.png"
			user_keys = ''

		if variables != orig_variables:
			orig_variables = variables
			with open('variables.json', 'w') as f:
				json.dump(variables, f)

		# RUNNIG THE ENGINE
		if not stopped:

			# CHECKING IF FOOD IS EATEN
			eaten_food = foods.eaten()
			if eaten_food != None:
				score += 1
				if score > variables['highscore']:
					variables['highscore'] = score
				foods.change_food(eaten_food)
				board.configure(text=board_text.replace('--', str(score)).replace('__', str(variables['highscore'])))

			# MOVING PACMAN
			pac_x += speed * dir['x']
			pac_y += speed * dir['y']

			if pac_x <= -24 or pac_x >= 773:
				pac_x = 773 - abs(pac_x)

			if outOfBound((pac_x, pac_y)):
				pac_x -= speed * dir['x']
				pac_y -= speed * dir['y']
			else:
				pac.place(x=pac_x, y=pac_y)

			# MOVING THE GHOSTS
			if not ghosts_stopped:
				my_ghost.move_ghosts(pac_dir=dir)

			# CHECKING COLLISION WITH GHOST
			if affected:
				if my_ghost.check_collision():
					times_touched += 1
					stopped = True
					tog.configure(image=play_img)
					valid = False
					while not valid:
						pac_x, pac_y = random_poss(object='pac')
						for ghost in my_ghost.ghosts:
							ghost_x, ghost_y = float(ghost.place_info()['x']), float(ghost.place_info()['y'])
							dx = abs(pac_x - ghost_x)
							dy = abs(pac_y - ghost_y)
							if dx > 60 and dy > 60:
								valid = True
					pac.place(x=pac_x, y=pac_y)

			# UPDATING LEVEL

			if score % score_boundary == score_boundary-2 and my_ghost.count < max_ghosts:
				for food in foods.foods:
					food.configure(image=food_colored_img)

			if score % score_boundary == score_boundary-1 and my_ghost.count < max_ghosts:
				my_ghost.create_ghost(speed=speed_ghost, movement_type='random')
				score += 1
				if score > variables['highscore']:
					variables['highscore'] = score
				board.configure(text=board_text.replace('--', str(score)).replace('__', str(variables['highscore'])))
				for food in foods.foods:
					food.configure(image=food_img)
			def play_again():
				canvas1.place_forget()
			def game_over():
				canvas1.place(x=250, y=100)


			canvas1 = tk.Canvas(width=300,height=300,bg='black')
			canvas1.create_image(150,100,image=game_over_img)
			play_button= tk.Button(canvas1,text='PLAY AGAIN',command=play_again,bg='black',fg='white')
			play_button.place(x=110,y=220)

			if times_touched == max_touches:
				# GAME LOST
				game_over()
				my_ghost.recreate(initial_n_of_ghosts)
				times_touched = 0
				score = 0
				board.configure(text=board_text.replace('--', str(score)).replace('__', str(variables['highscore'])))
		root.update()


	#Cheat Code Functions
	def CheatCode_1():
		#Code for CheatCode
		global user_keys
		user_keys += "easy"
		canvas.place_forget()

	def CheatCode_2():
		#Code for CheatCode
		global user_keys
		user_keys += "medium"
		canvas.place_forget()

	def CheatCode_3():
		#Code for CheatCode
		global user_keys
		user_keys += "hard"
		canvas.place_forget()

	def CheatCode_4():
		#Code for CheatCode
		global user_keys
		user_keys += "clip"
		canvas.place_forget()

	def CheatCode_5():
		#Code for CheatCode
		global user_keys
		user_keys += "affected"
		canvas.place_forget()

	def CheatCode_6():
		#Code for CheatCode
		global user_keys
		user_keys += "faster"
		canvas.place_forget()

	def CheatCode_7():
		#Code for CheatCode
		global user_keys
		user_keys += "slower"
		canvas.place_forget()

	def CheatCode_8():
		#Code for CheatCode
		global user_keys
		user_keys += "default"
		canvas.place_forget()

	def CheatCode_9():
		#Code for CheatCode
		global user_keys
		user_keys += "changemap"
		canvas.place_forget()


	#Creating Canvas fof Master Box
	canvas=tk.Canvas(width=400,height=400,bg='black')
	canvas.create_text(130, 30, text='List of Cheat codes:', font=('times', 20, 'bold'),fill='white')
	# Cheat code 1
	canvas.create_text(78, 70, text='Difficulty: Easy', font=('times', 15, 'bold'),fill='white')
	b1 = tk.Button(canvas, text='Activate', command=CheatCode_1,bg='black',fg='white')
	b1.place(x=300, y=60)
	# Cheat code 2
	canvas.create_text(91, 107, text='Difficulty: Medium', font=('times', 15, 'bold'),fill='white')
	b2 = tk.Button(canvas, text='Activate',command=CheatCode_2,bg='black',fg='white')
	b2.place(x=300, y=95)
	# Cheat code 3
	canvas.create_text(79, 140, text='Difficulty: Hard', font=('times', 15, 'bold'),fill='white')
	b3 = tk.Button(canvas, text='Activate',command=CheatCode_3,bg='black',fg='white')
	b3.place(x=300, y=130)

	# Cheat code 4
	canvas.create_text(60, 175, text='Clip Ghosts', font=('times', 15, 'bold'),fill='white')
	b4 = tk.Button(canvas, text='Activate',command=CheatCode_4,bg='black',fg='white')
	b4.place(x=300, y=165)

	# Cheat code 5
	canvas.create_text(100, 210, text='Invulnerable Pacman', font=('times', 15, 'bold'),fill='white')
	b5 = tk.Button(canvas, text='Activate',command=CheatCode_5,bg='black',fg='white')
	b5.place(x=300, y=200)

	# Cheat code 6
	canvas.create_text(75, 245, text='Faster Pacman', font=('times', 15, 'bold'),fill='white')
	b6 = tk.Button(canvas, text='Activate',command=CheatCode_6,bg='black',fg='white')
	b6.place(x=300, y=235)

	# Cheat code 7
	canvas.create_text(76, 280, text='Slower Pacman', font=('times', 15, 'bold'),fill='white')
	b7 = tk.Button(canvas, text='Activate',command=CheatCode_7,bg='black',fg='white')
	b7.place(x=300, y=270)

	# Cheat code 8
	canvas.create_text(78, 315, text='Default Settings', font=('times', 15, 'bold'),fill='white')
	b8 = tk.Button(canvas, text='Activate',command=CheatCode_8,bg='black',fg='white')
	b8.place(x=300, y=305)

	# Cheat code 9
	canvas.create_text(62, 350, text='Change Map', font=('times', 15, 'bold'),fill='white')
	b9 = tk.Button(canvas, text='Activate',command=CheatCode_9,bg='black',fg='white')
	b9.place(x=300, y=340)



	# CREATING BAR
	bar, tog, instruction, boss, board, filler = get_bar(root, imgs=[play_img, pause_img, instruction_img, boss_img, black_img])
	board.configure(text=board_text.replace('--', str(score)).replace('__', str(variables['highscore'])))
	def play_pause():
		global stopped
		if stopped == True:
			tog.configure(image=pause_img)
			stopped = False
		else:
			tog.configure(image=play_img)
			stopped = True

	def show_instructions():
		global stopped
		# display instruction box here
		tog.configure(image=play_img)
		stopped = True
		messagebox.showinfo('Instruction',"Direction of Pacman can be change by arrow keys \nPress spacebar to pause the game")

	def show_boss():
		global stopped
		tog.configure(image=play_img)
		stopped = True
		canvas.place(x=250, y=120)


	tog.configure(command=play_pause)
	instruction.configure(command=show_instructions)
	boss.configure(command=show_boss)


	# GAME LOOP
	for i in range(100000000):
		time.sleep(0.001)
		gameEngine()
	root.mainloop()
mainmenu = tk.PhotoImage(file='static/mainmanu.png')
start_img=tk.PhotoImage(file='static/start.png')
main_canvas = tk.Canvas(width=850,heigh=600,bg='black')
main_canvas.create_image(430,300,image=mainmenu)
bn =tk.Button(main_canvas,image=start_img,command=main_loop)
bn.place(x=370,y=400)
main_canvas.pack()
root.mainloop()