#!/usr/bin/env python3

# program to implement a very basic command-line version of the minesweeper game
#-------------------------------------------------------------------------------

import sys
import random

def main():

	print('Welcome to Minesweeper!\n')
	difficulty = get_difficulty()
	minecells  = allocate_mines(difficulty)
	grid       = draw_initial_grid(difficulty)

	print_grid(grid)
	while True:

		action = select_action()
		if action == "flag":
			grid = flag_mine(grid)
		elif action == "uncover":
			grid = uncover_square(grid, minecells)
		else:
			print("Thanks for Playing!")
			sys.exit()
		print_grid(grid)

		if check_victory(grid, minecells):
			print("YOU WIN! Nice Work, Bro")
			sys.exit()


def get_difficulty():

	valid = {"B","I","A"}
	message = ("[B] Beginner: 5x5 grid with 3 mines\n"
			   "[I] Intermediate: 10x10 grid with 10 mines\n"
			   "[A] Advanced: 20x20 grid with 40 mines\n")

	while True:
		print(message)
		difficulty = input("Please Select A Difficulty Level: ")
		if difficulty.strip().upper() in valid:
			return difficulty.strip().upper()
		else:
			print("Please Select A Valid Difficulty Level")


def allocate_mines(difficulty):

	if difficulty == "B":
		rows  = 5
		cols  = 5
		mines = 3
	elif difficulty == "I":
		rows  = 10
		cols  = 10
		mines = 10
	else:
		rows  = 20
		cols  = 20
		mines = 40

	minecells = []
	allocated = 0

	while allocated <= mines:

		minerow = random.randint(0,rows-1)
		minecol = random.randint(0,cols-1)

		if (minerow, minecol) in minecells:
			continue
		else:
			minecells.append((minerow, minecol))
			allocated += 1

	return minecells
	# this will be a list of tuples, where each tuple is a (row,col) location where a mine was randomly placed


def draw_initial_grid(difficulty):

	if difficulty == "B":
		dim = 5
	elif difficulty == "I":
		dim = 10
	else:
		dim = 20

	initial_grid = []
	for i in range(0,dim):
		initial_grid.append(["?" for j in range(0,dim)])

	return initial_grid
	# this will be a list of lists, where the outer list represents rows and the inner list represents columns within a row


def select_action():

	message = "\nPlease Select An Action: [1] - Flag A Square; [2] - Uncover a Square; [3] - Quit the Game"
	valid = {"1","2","3"}

	while True:
		print(message)
		action = input("Action: ")
		action = action.strip().upper()
		if action in valid:
			if action == "1":
				return "flag"
			elif action == "2":
				return "uncover"
			else:
				return "quit"
		else:
			print("Please Select A Valid Action")


def flag_mine(grid):

	while True:
		try:
			flagrow = input("Please Select a Row Number [1-N] to Flag: ")
			flagcol = input("Please Select a Col Number [1-N] to Flag: ")
			flagrow = int(flagrow) - 1
			flagcol = int(flagcol) - 1

			if grid[flagrow][flagcol] != "?":
				print("Cell ({0},{1}) Has Already Been Uncovered".format(flagrow+1, flagcol+1))
				return grid
			else:
				grid[flagrow][flagcol] = "\N{WHITE FLAG}"
				return grid

		except ValueError:
			print("Please Select a Valid Integer Row/Col Number")
			return grid
		except IndexError:
			print("Cell ({0},{1}) Is Not A Valid Grid Selection".format(flagrow+1, flagcol+1))
			return grid


def uncover_square(grid, minecells):

	while True:
		try:
			urow = input("Please Select a Row Number [1-N] to Uncover: ")
			ucol = input("Please Select a Col Number [1-N] to Uncover: ")
			urow = int(urow) - 1
			ucol = int(ucol) - 1

			if grid[urow][ucol] != "?":
				print("Cell ({0},{1}) Has Already Been Flagged or Uncovered".format(urow+1, ucol+1))
				return grid
			else:
				if (urow, ucol) in minecells:
					game_lost(grid, minecells)
				else:
					grid[urow][ucol] = "U"
					grid = update_grid(grid, minecells)
					return grid

		except ValueError:
			print("Please Select a Valid Integer Row/Col Number")
			return grid
		except IndexError:
			print("Cell ({0},{1}) Is Not A Valid Grid Selection".format(urow+1, ucol+1))
			return grid


def update_grid(grid, minecells):

	while True:
		newblanks = False
		for i in range(0,len(grid[0])):
			for j in range(0,len(grid[0])):

				if grid[i][j] == "U":
					adjcount = 0
					for a in range(-1,2):
						for b in range(-1,2):
							if (i+a, j+b) in minecells:
								adjcount += 1
					grid[i][j] = str(adjcount)

				if grid[i][j] == "0":
					grid[i][j] == " "
					for a in range(-1,2):
						for b in range(-1,2):
							if (0 <= i+a < len(grid[0])) and (0 <= j+b < len(grid[0])) and (grid[i+a][j+b] == "?"):
								grid[i+a][j+b] = "U"
								newblanks = True
		if newblanks == True:
			continue
		else:
			return grid


def print_grid(grid):

	hsep = "-" * ((len(grid[0])*2)+1)
	vsep = "|"

	print("\n", hsep, sep="")
	for row in grid:
		print(vsep, vsep.join(row), vsep, sep="")
		print(hsep)


def game_lost(grid, minecells):
	print("\nKABLOOM! YOU LOSE! Tough Break, Bro")
	grid = reveal_mines(grid, minecells)
	print_grid(grid)
	sys.exit()


def reveal_mines(grid, minecells):
	for i in range(0, len(grid[0])):
		for j in range(0, len(grid[0])):
			if (i, j) in minecells:
				grid[i][j] = "\N{RADIOACTIVE SIGN}"
	return grid


def check_victory(grid, minecells):

	any_uncovered = False
	flagged_squares = []

	for i in range(0, len(grid[0])):
		for j in range(0, len(grid[0])):

			if grid[i][j] == "?":
				any_uncovered = True
			if grid[i][j] == "\N{WHITE FLAG}":
				flagged_squares.append((i,j))

	if (any_uncovered == False) and (sorted(flagged_squares) == sorted(minecells)):
		return True
	else:
		return False

main()

