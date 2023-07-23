import json
with open('variables.json', 'r') as f:
	variables = json.load(f)

# VARIABLES
speed = 3
speed_increment = 0.5
speed_ghost = 1
speed_follower = 2
speed_ambush = 2
level_speed_increment = 0.7
ambush_distance = 140
max_ghosts = 5
score_boundary = 10
food_count = 5
max_touches = 3
initial_n_of_ghosts = 2
board_text = "\n\n\nS\nC\nO\nR\nE\n:\n--\n\nH\nI\nG\nH\nS\nC\nO\nR\nE\n:\n__"

maze_img_url = variables['maze_img_url']
pac_R_url = "Static/pacR.png"
pac_L_url = "Static/pacL.png"
pac_U_url = "Static/pacU.png"
pac_D_url = "Static/pacD.png"
pac_eaten_url = "Static/pac_eaten.png"
food_url = "Static/food.png"
food_colored_url = "Static/food-colored.png"
blue_url = "Static/blue.png"
pink_url = "Static/pink.png"
red_url = "Static/red.png"
yellow_url = "Static/yellow.png"
sky_url = "Static/sky.png"
brown_url = "Static/brown.png"
green_url = "Static/green.png"
play_url = "Static/play.png"
pause_url = "Static/pause.png"
instruction_url = "Static/instruction.png"
boss_url = "Static/boss.png"
black_url = "Static/black.png"

# CONSTANTS
width, height = 800, 600
pac_size = (24, 18)
food_size = (12, 12)
ghost_size = (20, 20)