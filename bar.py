import tkinter as tk
from constants import board_text

def get_bar(root, imgs):
	play_img, pause_img, instruction_img, boss_img, black_img = imgs

	# BAR
	bar = tk.Label(root, bd=0, width=52, height=600, background='black', borderwidth=0)
	bar.place(x=798, y=0)

	# BUTTONS HERE
	tog = tk.Button(bar, width=52, height=52, borderwidth=0, highlightthickness=0, image=play_img)
	tog.pack()

	instruction = tk.Button(bar, width=52, height=52, borderwidth=0, highlightthickness=0, image=instruction_img)
	instruction.pack()

	boss = tk.Button(bar, width=52, height=52, borderwidth=0, highlightthickness=0, image=boss_img)
	boss.pack()

	board = tk.Label(
		bar,
		text=board_text,
		fg='white',
		font=("Arial", 12),
		background='black',
		borderwidth=0,
		highlightthickness=0
	)
	board.pack()

	filler = tk.Button(bar, width=52, height=444, borderwidth=0, highlightthickness=0, image=black_img)
	filler.pack()
	# filler = 0

	return bar, tog, instruction, boss, board, filler