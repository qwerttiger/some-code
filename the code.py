#imports
import pygame,copy,os,sys,time

#pygame setup
pygame.init()

#image loading
playerright=pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/player.png")
playerleft=pygame.transform.flip(playerright,True,False)
playersmallleft=pygame.transform.scale(playerleft,(25,25))
playersmallright=pygame.transform.scale(playerright,(25,25))

#mask making (masks can tell you which things collide)
top=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/top.png"),(0,0,0),(1,1,1))
bottom=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/bottom.png"),(0,0,0),(1,1,1))
side=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/side.png"),(0,0,0),(1,1,1))
topsmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/topsmall.png"),(0,0,0),(1,1,1))
bottomsmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/bottomsmall.png"),(0,0,0),(1,1,1))
sidesmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/sidesmall.png"),(0,0,0),(1,1,1))

#pygame display setup
screen=pygame.display.set_mode((700,700))
pygame.display.set_caption("Platformer")

#variable setup
costume=playerright
xpos=0
ypos=550
level=1

#more mask setup
bigcharmask=pygame.mask.Mask((50,50),True)
smallcharmask=pygame.mask.Mask((25,25),True)

#more variable setup
xvel=0
yvel=0
big=True
gravity=1
canswitchg=True
listofdisplays=[(1,"hi","this is a platformer","left and right keys to move"),(2,"up to jump"),(3,"avoid red"),(4,"green makes you shrink"),(5,"blue makes you back to normal"),(6,"magenta makes you go right"),(8,"water!"),(9,"don't get stuck inside","oh by the way press \"r\" to reset"),(10,"a trampoline!"),(11,"press z to switch gravity")]

#function setup
def setmask(): #this sets which mask to use
  global charmask
  if big:
    charmask=bigcharmask
  else:
    charmask=smallcharmask

def draw(): #this draws the background
  screen.blit(pygame.image.load(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"),(0,0))

def drawchar(): #draws the character
  screen.blit(costume,(round(xpos),round(ypos)))

def maketomask(*things): #makes a string and colour to a mask
  for thing in things:
    name,colour=thing[0],thing[1]
    exec(f"global {name}",globals())
    exec(f"{name}=pygame.mask.from_threshold({name},{colour},(1,1,1))",globals())

def setuplvl(): #sets up the mask for level
  global ground,lava,jumpy,fastleft,fastright,water,shrink,normal,win
  file=pygame.image.load(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png")
  ground,lava,jumpy,fastleft,fastright,water,shrink,normal,win=copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file)
  maketomask(["ground",(0,0,0)],["lava",(255,0,0)],["jumpy",(255,255,100)],["fastleft",(0,255,0)],["fastright",(255,0,255)],["water",(0,255,255)],["shrink",(0,100,0)],["normal",(0,0,100)],["win",(255,255,0)])

def touchingmask(mask): #mask collide detection
  return bool(charmask.overlap(mask,(-round(xpos),-round(ypos))))

def touchingmask2(mask,diff): #more advanced mask collide detection
  return bool(mask.overlap(ground,(-round(xpos+diff[0]),-round(ypos+diff[1]))))

def drawtext(text,colour): #draws a single piece of text
  screen.blit(pygame.font.SysFont("arial",30).render(text,True,colour),(350-round(pygame.font.SysFont("arial",30).render(text,True,colour).get_width()/2),100-pygame.font.SysFont("arial",30).render(text,True,colour).get_height()/2))

def drawtexts(lists): #draw multiple texts
  for listt in lists: #for every given parameter
    if level==listt[0]: #if it is the given level
      thing=listt[1:] #then the list of things to draw is set to "thing"
      for InsertsRandomCharacter in thing: #for something in the list "thing"
        drawtext(InsertsRandomCharacter,(0,0,0)) #draw the thing it is supposed to draw
        pygame.display.flip() #update
        time.sleep(1) #waits
        drawtext(InsertsRandomCharacter,(255,255,255)) #delete the text
        for event in pygame.event.get(): #see if you quit
          if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

def startthing(): #the thing at the start
  screen.fill((255,255,255))
  drawtext("epik | a platformer",(0,0,0))
  pygame.draw.rect(screen,(0,0,0),pygame.Rect((300,300),(100,100)),1)
  pygame.draw.line(screen,(0,0,0),(328,325),(328,375))
  pygame.draw.line(screen,(0,0,0),(328,325),(361,350))
  pygame.draw.line(screen,(0,0,0),(328,375),(361,350))
  pygame.display.flip()
  keep_going=True
  while keep_going:
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type==pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos()[0]>=300 and pygame.mouse.get_pos()[0]<=400 and pygame.mouse.get_pos()[1]>=300 and pygame.mouse.get_pos()[1]<=400:
        keep_going=False

startthing()
while True: #level loop
  xvel,yvel=0,0 #set velocity to 0
  screen.fill((255,255,255))
  if os.path.exists(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"): #if the background picture exists
    setuplvl() #setup the level
    xpos,ypos=0,550 #setup the character position
    big=True #go bigger

  else: #if you went through all of the levels
    pygame.quit() #pygame exit
    input("\nYOU WON") #then you win
    sys.exit() #exit

  draw() #draw the background
  drawchar() #draw the character
  pygame.display.flip()
  #drawing text
  drawtexts(listofdisplays)

  while True: #main loop
    setmask() #setup the mask
    draw() #draw the background
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
      up_touch=touchingmask2(top,(0,1))
      down_touch=touchingmask2(bottom,(0,0))
      side_touch=touchingmask2(side,(1,0))

    else: #if the character is small (or not big)
      #collide with ground
      up_touch=touchingmask2(topsmall,(0,1))
      down_touch=touchingmask2(bottomsmall,(0,0))
      side_touch=touchingmask2(sidesmall,(1,0))

    #these lines makes friction
    if not side_touch:
      if xvel>1:
        xvel-=1
      elif xvel<-1:
        xvel+=1
      else:
        xvel=0

    if not ((down_touch and gravity==1) or (up_touch and gravity==-1)): #if not touching ground
      if not touch_water: #if not touching water
        yvel-=gravity #gravity
      else: #if touching water
        ypos+=gravity #go down
    else: #if touching ground
      ypos+=yvel-0.5*gravity #go up
      yvel=0 #and don't go down

    keys=pygame.key.get_pressed() #the keys that are pressed
    if side_touch: #if touching the side
      xvel=-xvel #then bounce
      xpos+=xvel #and go back
    if keys[pygame.K_UP] and ((down_touch and gravity==1) or (up_touch and gravity==-1)) and not touch_water: #if you press up while touching the ground and not touching the water
      yvel+=20*gravity #jump
    if keys[pygame.K_UP] and touch_water: #if you press up while touching water
      ypos-=3*gravity #swim
    if keys[pygame.K_LEFT]: #if pressing left
      xvel-=1.5 #accelerate left
      if big: #if you are big
        costume=playerleft #then set your costume to the big player left
      else: #if small
        costume=playersmallleft #set to small player left
    if keys[pygame.K_RIGHT]: #if pressing right
      xvel+=1.5 #go right
      if big: #if big
        costume=playerright #set costume to big player right
      else: #if small
        costume=playersmallright #set to small player right
    if keys[pygame.K_z] and level>=11 and ((down_touch and gravity==1) or (up_touch and gravity==-1)): #if switching gravity
      if canswitchg: #and if you can switch
        gravity=-gravity #reverse gravity
        canswitchg=False #and not be able to switch
    else: #else
      canswitchg=True #you can switch gravity
    if keys[pygame.K_r]:
      xvel,yvel,xpos,ypos=0,0,0,550

    #set the costume if not pressing left and right
    if not big and costume==playerleft:
      costume=playersmallleft
    if not big and costume==playerright:
      costume=playersmallright
    if big and costume==playersmallleft:
      costume=playerleft
    if big and costume==playersmallright:
      costume=playerright
    for event in pygame.event.get():
      if event.type==pygame.QUIT: #if you press quit
        pygame.quit() #then quit
        sys.exit() #and exit
    if xpos<0: #if touching edge
      xvel=-xvel #bounce
      xpos=0 #go back
    if xpos>650: #if touching other edge
      xvel=-xvel #bounce
      xpos=650 #go back

    if touch_lava: #if touching lava
      xpos,ypos=0,550 #then restart

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

    pygame.display.flip() #update

    if touch_win: #if you win
      level+=1 #go to next level
      break
