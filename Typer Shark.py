# Typer Shark
import turtle as trtl
import random as rand
import time

# setup:
# lists and variables:
sharks = []
letters = []
words = ['ace', 'arc', 'art', 'bee', 'boy', 'bug', 'car', 'cog', 'cup', 'day', 'dig', 'dog', 'duo', 'ear', 'eel', 'eve', 'fat', 'fee', 'fig', 'gap', 'gem', 'gum', 'hat', 'hop', 'hue', 'ice', 'ion', 'ill', 'jam', 'jar', 'jog', 'kid', 'kin', 'kit', 'lay', 'lid', 'log', 'mad', 'man', 'map', 'nag', 'nap', 'net', 'oat', 'odd', 'oil', 'pan', 'pod', 'pub', 'ran', 'rob', 'rug', 'saw', 'sax', 'sob', 'tan', 'toe', 'two', 'urn', 'van', 'vat', 'wad', 'wag', 'web', 'yaw', 'yep', 'yet', 'zag', 'zed', 'zoo']
divided_words = []
grabbed = []
normal_words = [] # additional "nice" features
impossible_words = []
score = -100
three_spaces = 3
health = 110
damage = -439/10
speed = 5

# screen and shark setup:
wn = trtl.Screen()
wn.tracer(False)
shark_image = 'shark.gif' # store the file name of your shape
defeated_shark_image = 'defeated-shark.gif'
shark_shock = 'shark-shock.gif'
reverse_shark = 'reverse-shark.gif'
shark_bite = 'shark-bite.gif'
submarine_image = 'submarine.gif'
torpedo_image = 'torpedo.gif'
wn.addshape(shark_image) # make the screen aware of the new file
wn.addshape(defeated_shark_image)
wn.addshape(shark_shock)
wn.addshape(reverse_shark)
wn.addshape(shark_bite)
wn.addshape(submarine_image)
wn.addshape(torpedo_image)
wn.bgpic('background.gif')
wn.setup(width=1280, height=720) # dimensions of the background file make it 600 x 400
wn.title('Typer Shark')

# create sharks:
num_sharks = len(words)
for num in range(0, num_sharks):
  shark = trtl.Turtle()
  sharks.append(shark)

# create string with words divided up:  
rand.shuffle(words)  
string = ''
for word in words:
  string += word

# create writer turtles for each character
for char in string:
  divided_words.append(char)
  writer = trtl.Turtle()
  writer.ht()
  writer.up()
  writer.color('black')
  letters.append(writer)

# create title turtle
title = trtl.Turtle()
title.ht()
title.pencolor('white')
title.up()
title.goto(435, 315)
title.write('Typer Shark', font=('Arial', 24, 'bold'))
title.down()

# create pause screen turtle
pause = trtl.Turtle()
pause.ht()

# create score_writer turtle
score_writer = trtl.Turtle()
score_writer.ht()
score_writer.pencolor('white')
score_writer.up()
score_writer.goto(-630, 315)
score_writer.down()

# create health_bar and damage turtle
health_bar = trtl.Turtle()
health_bar.ht()
health_bar.speed(0)
health_bg = trtl.Turtle()
health_bg.ht()
health_bg.pensize(1)
health_bg.pencolor('black')
health_bg.speed(0)
health_bg.up()
health_bg.goto(-630, -343)
health_bg.down()
health_bg.fillcolor('black')
health_bg.begin_fill()
health_bg.goto(-515, -343)
health_bg.goto(-490, -318)
health_bg.goto(-181, -318)
health_bg.goto(-181, -283)
health_bg.goto(-630, -283)
health_bg.end_fill()

# create submarine turtle
submarine = trtl.Turtle()
submarine.up()
submarine.seth(90)
submarine.goto(-350, 0)
submarine.shape(submarine_image)

# functions:
def create_shark(active_shark): # creates x number of sharks based on # of words
  for active_shark in sharks:
    active_shark.up()
    active_shark.goto(800, 225)
    active_shark.shape(shark_image)
  i = 0
  spacing = 0
  while i < num_sharks:
    x = sharks[i].xcor()
    y = sharks[i].ycor()
    spacing += 115
    if i % 5 == 0:
      spacing = 0
    sharks[i].goto(x, y - spacing)   
    i += 1
  wn.update()

def write_words(): # writes individual letters onto sharks to appear like full words
  i = 0
  ii = -1
  spacing = 0                     
  while i < len(divided_words):
    if i % 3 == 0:
      ii += 1
      spacing = 0
    letters[i].goto(sharks[ii].xcor() + spacing - 30, sharks[ii].ycor() - 30)
    letters[i].write(divided_words[i], move=False,  align='center', font=('Arial', 35, 'bold'))  
    grabbed.append(divided_words[i])
    spacing += 25
    i += 1

def find_letter(letter): # searches for each letter when key is pressed
  if letter in divided_words and grabbed.index(letter) == 0:
    wn.tracer(True)
    divided_words[divided_words.index(letter)] = ''
    grabbed.pop(0)
    letters[grabbed.index(letter)].clear()
    wn.tracer(False)
  else:
    update_health()

def swim(): # makes the sharks come forward periodically while testing for win condition
  global health, y_limit, lower, higher, speed
  lower = 0
  higher = 4
  while health > 0:
    if sharks[higher].shape() == defeated_shark_image:
      sharks[higher].ht()
      y_limit = 500
      lower += 5
      higher += 5
      

    # move sharks and letters across screen, move submarine up and down
    rand_shark = rand.randint(lower, higher)
    for turtle in letters:
      turtle.clear()
    sharks[rand_shark].backward(speed)
    submarine.forward(.75)
    write_words() # calls function to maintain them on the sharks
    shark_defeat() # test for fully typed words
    list_index = len(divided_words) - 1
    wn.update()
    time.sleep(.025)
    submarine.forward(.75)
    sharks[rand_shark].backward(speed)

    # makes submarine move up and down by switching the heading
    if submarine.ycor() > 40:
      submarine.seth(270)
    elif submarine.ycor() < -40:
      submarine.seth(90)

    # testing if sharks are close to submarine or not
    if sharks[rand_shark].xcor() < 50 and sharks[rand_shark].xcor() > 0 and sharks[rand_shark].heading() == 0:
      sharks[rand_shark].shape(shark_bite)
    elif sharks[rand_shark].xcor() < 0:
      update_health()
      sharks[rand_shark].shape(reverse_shark)
      sharks[rand_shark].goto(sharks[rand_shark].xcor() + 5, sharks[rand_shark].ycor())
      sharks[rand_shark].seth(180)
      sharks[rand_shark].backward(5)
    elif sharks[rand_shark].xcor() > 180 and sharks[rand_shark].heading() == 180:
      sharks[rand_shark].shape(shark_image)
      sharks[rand_shark].seth(0)
      sharks[rand_shark].backward(5)
    elif divided_words[list_index] == ' ': # win condition
      break

  # if all words are typed, then program executes win function—else loss
  if health > 0:
    win()
  else:
    lose()

def scorer(): # adds to score and updates score
  global score
  score += 100
  score_writer.clear()
  score_writer.write('Depth: ' + str(score), font=('Arial', 24, 'bold'))

def shark_defeat(): # function to identify fully typed words
  global three_spaces, y_limit, lower, higher
  spaces = divided_words.count('')
  if spaces == three_spaces:
    three_spaces += 3
    scorer()
    for i in range(int(spaces / 3 - 1), int(spaces / 3)): # shark shock 'animation'
      sharks[i].seth(270)
      sharks[i].shape(shark_shock)
      wn.update()
      time.sleep(.125)
      sharks[i].shape(shark_image)
      wn.update()
      time.sleep(.125)
      sharks[i].shape(shark_shock)
      wn.update()
      time.sleep(.25)
      sharks[i].shape(defeated_shark_image)
      wn.update()
      y_limit = sharks[i].ycor() + 25
  if three_spaces > 3: # clear sharks after they float up a certain distance
    for i in range(lower, higher + 1):
      if sharks[i].ycor() > y_limit or sharks[i].ycor() > 230:
        sharks[i].goto(2000, 0)
        sharks[i].ht()

      
def win(): # funciton executes upon winning
  title.up()
  title.goto(0, 0)
  title.write('You won!', align='center', font=('Arial', 50, 'bold'))
  time.sleep(.25)

def lose(): # function executes upon losing
  title.up()
  title.goto(0, 0)
  title.write('You lost!', align='center', font=('Arial', 50, 'bold'))
  time.sleep(.25)

def update_health(): # updates health as sharks attack and mistakes are made
  global health, damage
  health -= 10
  damage += 439/10
  health_bar.clear()
  health_bar.pencolor('white')
  health_bar.up()
  health_bar.goto(-625, -343)
  health_bar.write('Health: ' + str(health), font=('Arial', 16))
  if health > 70: # update health bar color as health decreases
    health_bar.pencolor('lime')
    health_bar.fillcolor('lime')
  elif health > 30:
    health_bar.pencolor('gold')
    health_bar.fillcolor('gold')
  else:
    health_bar.pencolor('firebrick')
    health_bar.fillcolor('firebrick')
  health_bar.begin_fill()
  health_bar.goto(-625, -312)
  health_bar.goto(-186 - damage, -312)
  health_bar.goto(-186 - damage, -288)
  health_bar.goto(-625, -288)
  health_bar.end_fill()
  
def pause_screen():
  pause.pencolor('black')
  pause.fillcolor('black')
  pause.begin_fill()
  pause.goto(2000, 2000)
  pause.goto(2000, -2000)
  pause.goto(-2000, -2000)
  pause.goto(-2000, 2000)
  pause.goto(2000, 2000)
  pause.end_fill()
  pause.pencolor('white')
  pause.up()
  pause.goto(0, 0)
  pause.write('Click anywhere to begin.', align='center', font=('Arial', 50, 'bold'))

def play(x, y): # creates play funciton for onscreenclick to work
  pause.clear()
  swim()

# alot of functions to identify each keyboard press 
def a():
  find_letter('a')

def b():
  find_letter('b')

def c():
  find_letter('c')

def d():
  find_letter('d')

def e():
  find_letter('e')

def f():
  find_letter('f')

def g():
  find_letter('g')

def h():
  find_letter('h')

def i():
  find_letter('i')

def j():
  find_letter('j')

def k():
  find_letter('k')

def l():
  find_letter('l')

def m():
  find_letter('m')

def n():
  find_letter('n')

def o():
  find_letter('o')

def p():
  find_letter('p')

def q():
  find_letter('q')

def r():
  find_letter('r')

def s():
  find_letter('s')

def t():
  find_letter('t')

def u():
  find_letter('u')

def v():
  find_letter('v')

def w():
  find_letter('w')

def x():
  find_letter('x')

def y():
  find_letter('y')

def z():
  find_letter('z')

# function calls and events:
create_shark(shark)
scorer()
update_health()
pause_screen()
wn.onscreenclick(play)
wn.onkeypress(a, 'a')
wn.onkeypress(b, 'b')
wn.onkeypress(c, 'c')
wn.onkeypress(d, 'd')
wn.onkeypress(e, 'e')
wn.onkeypress(f, 'f')
wn.onkeypress(g, 'g')
wn.onkeypress(h, 'h')
wn.onkeypress(i, 'i')
wn.onkeypress(j, 'j')
wn.onkeypress(k, 'k')
wn.onkeypress(l, 'l')
wn.onkeypress(m, 'm')
wn.onkeypress(n, 'n')
wn.onkeypress(o, 'o')
wn.onkeypress(p, 'p')
wn.onkeypress(q, 'q')
wn.onkeypress(r, 'r')
wn.onkeypress(s, 's')
wn.onkeypress(t, 't')
wn.onkeypress(u, 'u')
wn.onkeypress(v, 'v')
wn.onkeypress(w, 'w')
wn.onkeypress(x, 'x')
wn.onkeypress(y, 'y')
wn.onkeypress(z, 'z')
wn.listen()
wn.mainloop()