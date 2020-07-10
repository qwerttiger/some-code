#imports
import pygame,copy,os,sys
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
def touchingmask2(mask,diff1,diff2): #more advanced mask collide detection
  return bool(mask.overlap(ground,(-round(xpos+diff1),-round(ypos-diff2))))
while True: #level loop
  if os.path.exists(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"): #if the background picture exists
    setuplvl() #setup the level
    xpos,ypos=0,550 #setup the character position
    big=True #go bigger
  else: #if you went through all of the levels
    input("\nYOU WON") #then you win
    sys.exit() #exit
    pygame.quit() #pygame exit
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
      up_touch=touchingmask2(top,0,1)
      down_touch=touchingmask2(bottom,0,0)
      side_touch=touchingmask2(side,1,0)
    else: #if the character is small (or not big)
      #collide with ground
      up_touch=touchingmask2(topsmall,0,1)
      down_touch=touchingmask2(bottomsmall,0,0)
      side_touch=touchingmask2(sidesmall,1,0)
    #these lines makes friction
    if not side_touch:
      if xvel>1:
        xvel-=1
      elif xvel<-1:
        xvel+=1
      else:
        xvel=0
    if not down_touch: #if not touching ground
      if not touch_water: #if not touching water
        yvel-=1 #gravity
      else: #if touching water
        ypos+=1 #go down
    else: #if touching ground
      ypos+=yvel-0.5 #go up
      yvel=0 #and don't go down
    keys=pygame.key.get_pressed() #the keys that are pressed
    if side_touch: #if touching the side
      xvel=-xvel #then bounce
      xpos+=xvel #and go back
    if keys[pygame.K_UP] and down_touch and not touch_water: #if you press up while touching the ground and not touching the water
      yvel+=20 #jump
    if keys[pygame.K_UP] and touch_water: #if you press up while touching water
      ypos-=3 #swim
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
    if xpos<0: #if touching edge
      xvel=-xvel #bounce
      xpos=0 #go back
    if xpos>650: #if touching other edge
      xvel=-xvel #bounce
      xpos=650 #go back
    if touch_lava: #if touching lava
      xpos,ypos=0,550 #then restart
    if up_touch and not down_touch: #if touching something above but not down
      ypos+=1 #go down
      yvel=0 #set yvel to 0
    if touch_jumpy: #if touching bouncy thing
      yvel+=5 #bounce up
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
