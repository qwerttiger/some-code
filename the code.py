import os #import os, a tool for not printing pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide" #hide support prompt

import pygame,copy,sys,time,random #import pygame; copy, a tool for copying a file; sys, a tool for exiting without confirmation; and time, a tool for waiting and recording the time, and random, a tool for random numbers

pygame.init() #pygame setup

playerright=pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/player.png") #image loading
playerleft=pygame.transform.flip(playerright,True,False) #flip the original picture to make the left-facing picture
playersmallleft=pygame.transform.scale(playerleft,(25,25)) #small left
playersmallright=pygame.transform.scale(playerright,(25,25)) #small right

for x in [playerright,playerleft,playersmallleft,playersmallright]: #for loop
  x.set_colorkey((255,255,255)) #set the transparent colourkey

#mask making (masks can tell you which things collide)
top=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/top.png"),(0,0,0),(1,1,1))
bottom=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/bottom.png"),(0,0,0),(1,1,1))
side=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/side.png"),(0,0,0),(1,1,1))
topsmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/topsmall.png"),(0,0,0),(1,1,1))
bottomsmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/bottomsmall.png"),(0,0,0),(1,1,1))
sidesmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/sidesmall.png"),(0,0,0),(1,1,1))

bigcharmask=pygame.mask.Mask((50,50),True)
smallcharmask=pygame.mask.Mask((25,25),True)

#pygame display setup
screen=pygame.display.set_mode((700,700))
pygame.display.set_caption("Platformer")

#variable setup
costume=playerright #set costume to go right
xpos=0 #set x position
ypos=599 #set y position
level=1 #set level
xvel=0 #set x velocity
yvel=0 #set y velocity
big=True #big or small
gravity=1 #set gravity to down
canswitchg=True #set if you can switch gravity
listofdisplays=[(1,"hi","this is a platformer","left and right keys to move"),(2,"up to jump"),(3,"avoid red"),(4,"green makes you shrink"),(5,"blue makes you back to normal"),(6,"magenta makes you go right"),(8,"water!"),(9,"don't get stuck inside","oh by the way press \"r\" to reset"),(10,"a trampoline!"),(11,"press z to switch gravity"),(12,"if it's too hard, press \"n\"."),(13,"now the element is grass"),(14,"use your power of gravity"),(16,"lolllll")] #list of things to display
displaytime=0 #the time it took to display
skips=0 #number of skips
deaths=0 #number of deaths
element="normal" #the element
lorr="right" #left-facing or right-facing

#function setup

def setmask(): #this sets which mask to use
  global charmask #set the charmask to a global variable
  if big: #if you are big
    charmask=bigcharmask #set to big mask
  else: #if you are small
    charmask=smallcharmask #set the mask to the small mask

def draw(): #this draws the background
  screen.blit(pygame.image.load(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"),(0,0))

def drawchar(): #draws the character
  screen.blit(costume,(round(xpos),round(ypos)))

def maketomask(*things): #makes a string and colour to a mask
  for thing in things: #for everything in the things
    name,colour=thing[0],thing[1] #the name and colour
    exec(f"global {name}",globals()) #global name
    exec(f"{name}=pygame.mask.from_threshold({name},{colour},(1,1,1))",globals()) #name=mask

def setuplvl(): #sets up the masks for the level
  global ground,lava,jumpy,fastleft,fastright,water,shrink,normal,win #global variables
  file=pygame.image.load(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png") #the level file
  ground,lava,jumpy,fastleft,fastright,water,shrink,normal,win=copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file) #set everything to copies of the file
  maketomask(["lava",(255,0,0)],["jumpy",(255,255,100)],["fastleft",(0,255,0)],["fastright",(255,0,255)],["water",(0,255,255)],["shrink",(0,100,0)],["normal",(0,0,100)],["win",(255,255,0)]) #make them to masks

  if not element=="grass": #if not element is grass
    maketomask(["ground",(0,0,0)]) #set ground mask
  if element=="grass": #if it is grass
    maketomask(["ground",(0,200,0)]) #set ground mask

def touchingmask(mask): #mask collide detection
  return bool(charmask.overlap(mask,(-round(xpos),-round(ypos))))

def touchingmask2(mask,diff): #more advanced mask collide detection
  return bool(mask.overlap(ground,(-round(xpos+diff[0]),-round(ypos+diff[1]))))

def drawtext(text,colour,size=30,pos=(350,100)): #draws a single piece of text
  screen.blit(pygame.font.SysFont("arial",size).render(text,True,colour),(pos[0]-round(pygame.font.SysFont("arial",size).render(text,True,colour).get_width()/2),pos[1]-pygame.font.SysFont("arial",size).render(text,True,colour).get_height()/2))
  return pygame.font.SysFont("arial",size).render(text,True,colour)

def drawtexts(lists): #draw multiple texts
  for listt in lists: #for every given parameter
    if level==listt[0]: #if it is the given level
      thing=listt[1:] #then the list of things to draw is set to "thing"
      for x in thing: #for something in the list "thing"
        y=drawtext(x,(0,0,0)) #draw the thing it is supposed to draw
        pygame.display.flip() #update
        time.sleep(1) #waits
        pygame.draw.rect(screen,(255,255,255),pygame.Rect((350-round(y.get_width()/2),100-round(y.get_height()/2)),(y.get_width(),y.get_height()))) #delete the text
        for event in pygame.event.get(): #see if you quit
          if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

def displaytime_():
  global displaytime #set displaytime to be global
  for x in listofdisplays: #for everything in displays
    displaytime+=len(x[1:]) #change displaytime by the number of things to display

def displaytime__(level):
  x=0
  for y in range(len(listofdisplays)):
    if listofdisplays[y][0]<=level:
      x+=len(listofdisplays[y][1:])
  return x


def startthing(): #the thing at the start
  global playerright,playerleft,playersmallleft,playersmallright,t #set everything to be global
  ctime=time.time() #current time

  screen.fill((255,255,255)) #fill screen
  drawtext("elements | a platformer",(0,0,0),50) #draw text
  #drawing play button
  pygame.draw.rect(screen,(0,0,0),pygame.Rect((300,300),(100,100)),1)
  pygame.draw.line(screen,(0,0,0),(336,325),(336,375))
  pygame.draw.line(screen,(0,0,0),(336,325),(379,350))
  pygame.draw.line(screen,(0,0,0),(336,375),(379,350))
  pygame.draw.rect(screen,(0,0,0),pygame.Rect((100,300),(100,100)),1)
  screen.blit(playerright,(125,325)) #draw player

  pygame.display.flip() #flip screen
  keep_going=True #set keep_going

  while keep_going: #while you keep going
    for event in pygame.event.get(): #for every event
      if event.type==pygame.QUIT: #if quit
        pygame.quit() #quit
        sys.exit() #exit

      if (event.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0]>=300 and pygame.mouse.get_pos()[0]<=400 and pygame.mouse.get_pos()[1]>=300 and pygame.mouse.get_pos()[1]<=400) or event.type==pygame.KEYDOWN: #if you press play
        keep_going=False #go to the main game
        t+=time.time()-ctime #add the time it took for you to press start to subrtact the elapsed time by the time it took

      if event.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0]>=100 and pygame.mouse.get_pos()[0]<=300 and pygame.mouse.get_pos()[1]>=300 and pygame.mouse.get_pos()[1]<=400:
        #draw the screen
        screen.fill((255,255,255))
        pygame.draw.rect(screen,(0,0,0),pygame.Rect((175,325),(50,50)))
        pygame.draw.rect(screen,(255,0,0),pygame.Rect((225,325),(50,50)))
        pygame.draw.rect(screen,(0,255,0),pygame.Rect((275,325),(50,50)))
        pygame.draw.rect(screen,(0,0,255),pygame.Rect((325,325),(50,50)))
        pygame.draw.rect(screen,(255,255,0),pygame.Rect((375,325),(50,50)))
        pygame.draw.rect(screen,(255,0,255),pygame.Rect((425,325),(50,50)))
        pygame.draw.rect(screen,(0,255,255),pygame.Rect((475,325),(50,50)))
        pygame.display.flip() #flip display
        kep_going=True #lol keep_going but... yeah
        while kep_going: #while keep going
          for event in pygame.event.get(): #for every event
            if event.type==pygame.QUIT: #if you quit
              pygame.quit() #quit
              sys.exit() #exit
            if event.type==pygame.MOUSEBUTTONDOWN: #if you click
              pos=pygame.mouse.get_pos() #you find the position of the mouse

              if pos[1]>=325 and pos[1]<=375: #if you click in the region horizontal region where it works
                if pos[0]>=175 and pos[0]<225: #if you click on black
                  for posx in range(50): #for every column
                    for posy in range(50): #for every pixel in that column
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]: #if it is not blank
                        playerright.set_at((posx,posy),(0,0,0)) #set that pixel to black
                #the same for the other ones but with different colours

                if pos[0]>=225 and pos[0]<275:
                  for posx in range(50):
                    for posy in range(50):
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]:
                        playerright.set_at((posx,posy),(255,0,0))

                if pos[0]>=275 and pos[0]<325:
                  for posx in range(50):
                    for posy in range(50):
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]:
                        playerright.set_at((posx,posy),(0,255,0))

                if pos[0]>=325 and pos[0]<375:
                  for posx in range(50):
                    for posy in range(50):
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]:
                        playerright.set_at((posx,posy),(0,0,255))

                if pos[0]>=375 and pos[0]<425:
                  for posx in range(50):
                    for posy in range(50):
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]:
                        playerright.set_at((posx,posy),(255,255,0))

                if pos[0]>=425 and pos[0]<475:
                  for posx in range(50):
                    for posy in range(50):
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]:
                        playerright.set_at((posx,posy),(255,0,255))

                if pos[0]>=475 and pos[0]<525:
                  for posx in range(50):
                    for posy in range(50):
                      if playerright.get_at((posx,posy)) not in [(255,255,255),(254,254,254)]:
                        playerright.set_at((posx,posy),(0,255,255))

                playerleft=pygame.transform.flip(playerright,True,False) #set the new playerleft
                playersmallleft=pygame.transform.scale(playerleft,(25,25)) #and the new playersmallleft
                playersmallright=pygame.transform.scale(playerright,(25,25)) #and playersmallright

                for x in [playerright,playerleft,playersmallleft,playersmallright]: #for everything in this list
                  x.set_colorkey((255,255,255)) #set the colourkey

              #draw the things
              screen.fill((255,255,255))
              drawtext("elements | a platformer",(0,0,0),50)
              pygame.draw.rect(screen,(0,0,0),pygame.Rect((300,300),(100,100)),1)
              pygame.draw.line(screen,(0,0,0),(336,325),(336,375))
              pygame.draw.line(screen,(0,0,0),(336,325),(379,350))
              pygame.draw.line(screen,(0,0,0),(336,375),(379,350))
              pygame.draw.rect(screen,(0,0,0),pygame.Rect((100,300),(100,100)),1)
              screen.blit(playerright,(125,325))

              kep_going=False #exit this loop
              pygame.display.flip() #flip screen

#main game

displaytime_() #set the time it took to display
t=time.time() #set t to be the time
startthing() #do the thing at the start

while True: #level loop
  if level==13: #if the level is 13
    element="grass" #set the element to grass

  xvel,yvel=0,0 #set velocity to 0
  screen.fill((255,255,255)) #fill the screen
  if os.path.exists(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"): #if the background picture exists
    setuplvl() #setup the level
    xpos,ypos,gravity=0,599,1 #setup the character position
    big=True #go bigger
    costume=playerright #set the costume

  else: #if you went through all of the levels
    pygame.quit() #pygame exit
    input("you took "+str(round(time.time()-t-displaytime,1))+" seconds to win with "+str(skips)+" skips and "+str(deaths)+" deaths.") #then you win
    sys.exit() #exit

  draw() #draw the background
  drawchar() #draw the character

  if element=="grass": #if the element is grass
    pygame.draw.circle(screen,(255,255,1),(700,0),100) #draw the sun
  pygame.display.flip() #flip screen

  drawtexts(listofdisplays) #drawing text

  while True: #main loop
    setmask() #setup the mask
    draw() #draw the background

    if element=="grass": #if the element is grass
      pygame.draw.circle(screen,(255,255,1),(700,0),100) #draw the sun

    drawchar() #draw the character

    #level mask setup
    touch_lava=touchingmask(lava)
    touch_jumpy=touchingmask(jumpy)
    touch_fastleft=touchingmask(fastleft)
    touch_fastright=touchingmask(fastright)
    touch_water=touchingmask(water)
    touch_shrink=touchingmask(shrink)
    touch_normal=touchingmask(normal)
    touch_win=touchingmask(win)

    if big: #if the character is big (or not small)
      #collide with ground
      up_touch=touchingmask2(top,(0,1)) #set the up_touch,
      down_touch=touchingmask2(bottom,(0,0)) #down_touch,
      side_touch=touchingmask2(side,(1,0)) or xpos<0 or xpos>650 #and side_touch

    else: #if the character is small (or not big)
      #collide with ground
      up_touch=touchingmask2(topsmall,(0,1)) #set the up_touch,
      down_touch=touchingmask2(bottomsmall,(0,0)) #down_touch,
      side_touch=touchingmask2(sidesmall,(1,0)) or xpos<0 or xpos>675 #and side_touch

    #these lines makes friction
    if not side_touch: #if you are not touching the side
      if xvel>1: #if you are going right
        xvel-=1 #slow down
      elif xvel<-1: #if you are going left
        xvel+=1 #slow down
      else: #if you are going left or right very slowly
        xvel=0 #don't move

    if not ((down_touch and gravity==1) or (up_touch and gravity==-1)): #if not touching ground
      if not touch_water: #if not touching water
        yvel-=gravity #gravity
      else: #if touching water
        ypos+=gravity #go down
    else: #if touching ground
      ypos+=yvel-gravity #go up
      yvel=0 #and don't go down

    if side_touch: #if touching the side
      xvel=-xvel #then bounce
      xpos+=xvel #and go back

    keys=pygame.key.get_pressed() #the keys that are pressed

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and ((down_touch and gravity==1) or (up_touch and gravity==-1)) and not touch_water: #if you press up while touching the ground and not touching the water
      yvel+=20*gravity #jump
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and touch_water: #if you press up while touching water
      ypos-=3*gravity #swim
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: #if pressing left
      xvel-=1.25 #accelerate left
      lorr="left" #left
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: #if pressing right
      xvel+=1.25 #go right
      lorr="right" #right

    if keys[pygame.K_z] and level>=11 and ((down_touch and gravity==1) or (up_touch and gravity==-1)): #if switching gravity
      if canswitchg: #and if you can switch
        gravity=-gravity #reverse gravity
        canswitchg=False #and not be able to switch
    else: #else
      canswitchg=True #you can switch gravity

    if keys[pygame.K_r]: #if restart
      xvel,yvel,xpos,ypos,gravity,big=0,0,0,599,1,True
      if keys[pygame.K_e]: #if hard restart
        level=1 #restart level
        element="normal" #switch element to normal
        t=time.time() #restart the time
        break #and break out of main loop

    if keys[pygame.K_n]: #if skip level
      t_=time.time() #set t_ to current time
      level+=1 #add 1 to levels
      skips+=1 #change skips by 1
      while pygame.key.get_pressed()[pygame.K_n]: #while you are pressing n
        for event in pygame.event.get(): #for every event
          if event.type==pygame.QUIT: #if you quit
            pygame.quit() #quit
            sys.exit() #exit
      t+=time.time()-t_ #add starting time by current elapsed time so real elapsed time goes down
      break #break out of main loop

    if keys[pygame.K_b] and level!=1: #if skip level
      level-=1 #subtract 1 from levels
      while pygame.key.get_pressed()[pygame.K_b]: #while you are pressing b
        for event in pygame.event.get(): #for every event
          if event.type==pygame.QUIT: #if you quit
            pygame.quit() #quit
            sys.exit() #exit
      t+=time.time()-t_ #add starting time by current elapsed time so real elapsed time goes down
      break #break out of main loop

    if keys[pygame.K_p]: #if pause
      startthing() #do the start thing

    #set the costume
    if not big and lorr=="left":
      costume=playersmallleft
    if not big and lorr=="right":
      costume=playersmallright
    if big and lorr=="left":
      costume=playerleft
    if big and lorr=="right":
      costume=playerright

    for event in pygame.event.get():
      if event.type==pygame.QUIT: #if you press quit
        pygame.quit() #then quit
        sys.exit() #and exit

    if touch_lava or (ypos<=0 and gravity==-1) or ((ypos>=650 and gravity==1 and big) or (ypos>=675 and gravity==1)): #if touching lava or falling off the screen
      xpos,ypos,xvel,yvel,gravity=0,599,0,0,1 #then restart
      deaths+=1 #add 1 to deaths

    if (up_touch and not down_touch and gravity==1 and canswitchg) or (down_touch and not up_touch and gravity==-1 and canswitchg): #if touching something above but not down
      ypos+=1 #go down
      yvel=0 #set yvel to 0

    if touch_jumpy: #if touching bouncy thing
      yvel+=5*gravity #bounce up

    if touch_fastleft: #if touching fastleft
      xvel-=3 #accelerate left

    if touch_fastright: #if touching fastright
      xvel+=3 #accelerate right

    if touch_shrink: #if touching shrink block
      big=False #shrink

    if touch_normal: #if touching normal block
      big=True #go to normal

    if touch_water: #if touching water
      yvel=0 #set yvel to 0

    #move by the velocity
    xpos+=xvel
    ypos-=yvel

    screen.blit(pygame.font.SysFont("arial",20).render("level: "+str(level)+" time: "+str(round(time.time()-t-displaytime__(level)))+" deaths: "+str(deaths),1,(random.randint(0,255),random.randint(0,255),random.randint(0,255))),(0,0)) #draw usefull stuff like level, deaths, and time

    pygame.display.flip() #update

    if touch_win: #if you win
      level+=1 #go to next level
      break #break out of loop
