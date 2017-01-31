# Python game: Snow leopard vs Billy goats start up code
# Snow Leopards are played by the computer
# Billy Goats are played by human
# Advanced solution has the option of swapping the above or human vs human or computer vs computer

from graphics import *
import math
import random
import time

wSize = 800

possMoves = {
				0:[1,8,7],
				1:[2,9,0],
				2:[3,10,1],
				3:[2,11,4],
				4:[3,12,5],
				5:[4,13,6],
				6:[5,14,7],
				7:[6,15,0],
				8:[0,9,16,15],
				9:[1,10,17,8],
				10:[2,11,18,9],
				11:[3,12,19,10],
				12:[4,13,20,11],
				13:[5,14,21,12],
				14:[6,15,22,13],
				15:[7,8,23,14],
				16:[8,17,23],
				17:[9,18,16],
				18:[10,19,17],
				19:[11,20,18],
				20:[12,21,19],
				21:[13,22,20],
				22:[14,23,21],
				23:[15,16,22]
			 }

Leaps = {
			0:[2,16,6],
			1:[17],
			2:[4,18,0],
			3:[19],
			4:[6,20,2],
			5:[21],
			6:[0,22,4],
			7:[23],
			8:[10,14],
			9:[],
			10:[8,12],
			11:[],
			12:[10,14],
			13:[],
			14:[12,8],
			15:[],
			16:[18,0,22],
			17:[1],
			18:[20,2,16],
			19:[3],
			20:[22,4,18],
			21:[5],
			22:[20,6,16],
			23:[7]
		}

class Goat:
	def __init__(self, index, image):
		self.index = index
		self.image = image

class Leopard:
	def __init__(self, index, image):
		self.index = index
		self.image = image


# the main function should control the flow of the program, allow the players to place the Goats and Leopards and decide who has won
# it uses the random function for placing the Leopards
def main():
	win = GraphWin('Snow leopard vs Billy goats ',wSize,wSize)
	win.setBackground('green')
	win.setCoords(0,0,wSize,wSize)
	ptList = drawBoard(win)
	GoatsOccup = []
	LeopardsOccup = []
	unOccup = list(range(0,24))
	GoatPieces = []
	LeopardPieces = []
	notify = Text(Point(wSize/2,40), 'Goats Turn')
	notify.setTextColor('blue')
	notify.draw(win)

	place_pieces(win, notify, ptList, LeopardsOccup, LeopardPieces, unOccup, GoatPieces, GoatsOccup)
	game_loop(win, notify, ptList, LeopardsOccup, LeopardPieces, unOccup, GoatPieces, GoatsOccup)
	
def place_pieces(win, notify, ptList, LeopardsOccup, LeopardPieces, unOccup, GoatPieces, GoatsOccup):
	for i in range(3):
		# let human place goats
		human_place_goats(notify,GoatsOccup,unOccup,ptList,GoatPieces,win,LeopardsOccup)

		# let the computer place Snow Leopards
		computer_place_snow_leopards(notify,LeopardsOccup,unOccup,ptList,LeopardPieces,win)


def game_loop(win, notify, ptList, LeopardsOccup, LeopardPieces, unOccup, GoatPieces, GoatsOccup):
	leopards_win = False
	goats_win = False

	while(not (leopards_win or goats_win)):
		# let the human move a Goat
		leopards_win = moveGoat(notify,GoatsOccup,unOccup,ptList,GoatPieces,win)

		# let the computer move a Leopard
		goats_win = AImoveLeopard(notify,LeopardsOccup,unOccup,ptList,LeopardPieces,win,GoatsOccup)

	
	if leopards_win:
		print ("SNOW LEOPARDS WIN")
		notify.setText("SNOW LEOPARDS WIN")
	elif goats_win:
		print ("GOATS WIN")
		notify.setText("GOATS WIN")
	else:
		print ("BUG - game ended with no winner")
	

def moveGoat(notify,GoatsOccup,unOccup,ptList,GoatPieces,win):
	if len(GoatsOccup) == 0:
		return True					# Leopards win because there are no goats left!!

	found_goat = False
	clicked_goat = None				#will store the goat object that was clicked
	notify.setText("Move a Goat")
	print ("\nmove a goat")

	while not found_goat:
		point = win.getMouse()
		clicked_index, dist = findNN(point,ptList)

		print ("clicked on index: ", clicked_index)

		for g in GoatsOccup:
			if g.index == clicked_index:
				print ("clicked on a goat! checking to see if it can move...")

				goat_not_blocked = False 			#make sure the goat isn't blocked in all directions by other pieces
				goat_moves = possMoves[g.index]

				for index in goat_moves:
					if index in unOccup:
						print ("the goat can move! success")

						clicked_goat = g
						found_goat = True
					else:
						print ("clicked on a blocked goat! select another one")
						notify.setText("You clicked on a goat that can't move. Select another!")


	print ("selected goat at index: ", g.index)

	notify.setText("selected goat at "+ str(g.index))

	red_dot = Circle(ptList[clicked_index], 8)
	red_dot.setFill("red")
	red_dot.draw(win)

	start_location 		= clicked_goat.index	

	index_to_move = -1
	valid_move = False

	while not valid_move:
		point = win.getMouse()
		clicked_index, dist = findNN(point,ptList)

		print ("clicked on index: ", clicked_index)

		if clicked_index in unOccup and clicked_index in possMoves[start_location]:
			valid_move = True
			index_to_move = clicked_index
			print ("moving goat from ", g.index, "to ", index_to_move)

		notify.setText("selected goat at "+ str(g.index)+"\tselect a valid move!")

	print ("executing the movement...")

	start_location 		= clicked_goat.index		
	clicked_goat.index 	= index_to_move
	
	print ("updating unOccup")

	unOccup.append(start_location)			#no longer occupied
	unOccup.remove(index_to_move)			#new location occupied

	notify.setText("Moving goat from %d to %d" % (start_location, index_to_move))

	red_dot.undraw()

	move_piece(clicked_goat, start_location, index_to_move, ptList)		#do the animation	

	return False 		#leopards didn't win this round, because a movement was performed!



def human_place_goats(notify,GoatsOccup,unOccup,ptList,GoatPieces,win,LeopardsOccup):
	#This fucntion is used to display a text a box to notify user to place 4 goats and the function stores the point of
	# click to GoatsOccupy list

	print ("\nplace some goats")
	loop_count = 0
	while loop_count <4:
		print ("place goat number ", loop_count+1)
		notify.setText("Place %d Goat" %(loop_count+1))
		point = win.getMouse()
		#print(int(point.getX()),point.getY())
		index, dist = findNN(point,ptList)
		#print("printing index and point in list ")
		click = ptList[index]
		#print(ptList[index].getX(),ptList[index].getY())
		goat_img = Image(Point(click.getX(),click.getY()), "goatnew.gif")
		goat_img.draw(win)
		GoatsOccup.append(Goat(index, goat_img))

		print ("placed goat at ", index, goat_img)
		print(GoatsOccup)

		try:
			unOccup.remove(index)
			loop_count += 1
		except ValueError:
			goat_img.undraw()
			del GoatsOccup[-1]
			continue


def AImoveLeopard(notify,LeopardsOccup,unOccup,ptList,LeopardPieces,win,GoatsOccup):
	print ("\nMove a leopard")
	
	notify.setText("computer moving leopard...")

	random.shuffle(LeopardsOccup)	#randomise the list of leopards

	for leopard in LeopardsOccup:
		#check to see if leopard can eat a goat

		start_index = leopard.index
		possible_leaps = Leaps[start_index]		#where the leopard can leap
		goat_to_eat = None

		#SEE IF THERE ARE GOATS AROUND THE LEOPARD


		surrounding_locs = possMoves[start_index]

		random.shuffle(surrounding_locs)		#make sure it doesn't jump the same direction first each time

		for goat in GoatsOccup:
			if goat.index in surrounding_locs:
				nearby_goat = goat 				#goat is nearby! can we eat it?		placeholder variable to make names nicer

				goat_surrounding_area = possMoves[nearby_goat.index]

				#if the goat can get eaten....
				for location in goat_surrounding_area:
					if location in possible_leaps and location in unOccup:
						print ("found a goat to eat!!!!")

						#move the leopard
						leopard.index = location
						unOccup.append(start_index)
						unOccup.remove(location)
						move_piece(leopard, start_index, location, ptList)		#do the animation


						#goat eaten - spot unoccupied					
						unOccup.append(nearby_goat.index)
						#delete the goat!
						nearby_goat.image.undraw()
						GoatsOccup.remove(nearby_goat)
						#refresh board

						return False 		#leopard did a leap - goats didn't win this round



	for leopard in LeopardsOccup:
		#check to see if leopard can move

		start_index = leopard.index

		possible_moves = possMoves[start_index]
		random.shuffle(possible_moves)

		for dest_index in possible_moves:
			if dest_index in unOccup:
				leopard.index = dest_index

				unOccup.append(start_index)
				unOccup.remove(dest_index)

				move_piece(leopard, start_index, dest_index, ptList)		#do the animation

				return False 		#leopard did a movement - goats didn't win this round

	return True		#goats win because leopard couldnt eat a goat or move (i.e. all leopards were blocked)



def computer_place_snow_leopards(notify,LeopardsOccup,unOccup,ptList,LeopardPieces,win):
	print ("\nplace a leopard")
	notify.setText("Place a leopard (computer)")

	index = random.choice(unOccup)
	pt = ptList[index]
	#print(ptList[index].getX(),ptList[index].getY())
	leopard_img = Image(Point(pt.getX(),pt.getY()), "leopardnew.gif")
	leopard_img.draw(win)
	LeopardsOccup.append(Leopard(index, leopard_img))

	print ("placed leopard at ", index)

	unOccup.remove(index)


def move_piece(piece, start_i, destination_i, ptList):
	start = ptList[start_i]
	destination = ptList[destination_i]

	image = piece.image
	x1 = destination.getX()
	x2 = start.getX()
	y1 = destination.getY()
	y2 = start.getY()
	dx = (x1-x2)
	dy = (y1-y2)

	for u in range(100):
		image.move(dx/100,dy/100)
		time.sleep(0.01)


def drawBoard(win): # It draws the board and returns a list of Points (24 points)
	bk = wSize/8 # block size
	ptList = []
	for i in range(1,4):
		ptList = ptList + [Point(bk*i,bk*i), Point(bk*i,4*bk), Point(bk*i,bk*(8-i)),Point(4*bk,bk*(8-i)),
					   Point(bk*(8-i),bk*(8-i)),Point(bk*(8-i), 4*bk), Point(bk*(8-i),bk*i),Point(4*bk,bk*i)]
		pp = Polygon(ptList[-8:])
		pp.setWidth(5)
		pp.setOutline(color_rgb(255,255,0))
		pp.draw(win)
	for i in range(8):
		ll = Line(ptList[i],ptList[i+16])
		ll.setWidth(5)
		ll.setFill(color_rgb(255,255,0))
		ll.draw(win)
	return ptList

def findNN(pt, ptList): # returns the index number and distance of the nearest point from pt
	# finds the nearest valid location on the board to the (clicked) pt in ptList. This allows the use to click near the location and not    
	# pricesly on top of the locaion to place/select/move a piece. It returns the distance d and the index location nn in ptList of the nearest point.
	d = wSize * 2
	nn = -1
	for position , point in enumerate(ptList):
		dist = math.sqrt((pt.getX()-point.getX()) ** 2 + (pt.getY() - point.getY()) ** 2 )
		if dist < d:
			d = dist
			nn = position

	return nn , d

 
  
main()
	
	
	
