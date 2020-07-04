import pygame,copy,os,sys
pygame.init()
playerright=pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/player.png")
playerleft=pygame.transform.flip(playerright,True,False)
playersmallleft=pygame.transform.scale(playerleft,(25,25))
playersmallright=pygame.transform.scale(playerright,(25,25))
top=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/top.png"),(0,0,0),(1,1,1))
bottom=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/bottom.png"),(0,0,0),(1,1,1))
side=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/side.png"),(0,0,0),(1,1,1))
topsmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/topsmall.png"),(0,0,0),(1,1,1))
bottomsmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/bottomsmall.png"),(0,0,0),(1,1,1))
sidesmall=pygame.mask.from_threshold(pygame.image.load("C:/Users/Rainbow/Desktop/python/platformer sprites/sidesmall.png"),(0,0,0),(1,1,1))
screen=pygame.display.set_mode((700,700))
pygame.display.set_caption("Platformer")
costume=playerright
xpos=0
ypos=550
level=1
bigcharmask=pygame.mask.Mask((50,50),True)
smallcharmask=pygame.mask.Mask((25,25),True)
xvel=0
yvel=0
big=True
def setmask():
  global charmask
  if big:
    charmask=bigcharmask
  else:
    charmask=smallcharmask
def draw():
  try:
    screen.blit(pygame.image.load(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"),(0,0))
  except:
    pass
def drawchar():
  screen.blit(costume,(round(xpos),round(ypos)))
def maketomask(*things):
  for thing in things:
    name,colour=thing[0],thing[1]
    exec(f"global {name}",globals())
    exec(f"{name}=pygame.mask.from_threshold({name},{colour},(1,1,1))",globals())
def setuplvl():
  global ground,lava,jumpy,fastleft,fastright,water,shrink,normal,win
  file=pygame.image.load(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png")
  ground,lava,jumpy,fastleft,fastright,water,shrink,normal,win=copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file),copy.copy(file)
  maketomask(["ground",(0,0,0)],["lava",(255,0,0)],["jumpy",(255,255,100)],["fastleft",(0,255,0)],["fastright",(255,0,255)],["water",(0,255,255)],["shrink",(0,100,0)],["normal",(0,0,100)],["win",(255,255,0)])
def touchingmask(mask):
  return bool(charmask.overlap(mask,(-round(xpos),-round(ypos))))
def touchingmask2(mask,diff1,diff2):
  return bool(mask.overlap(ground,(-round(xpos+diff1),-round(ypos-diff2))))
while True:
  if os.path.exists(f"C:/Users/Rainbow/Desktop/python/platformer sprites/level {level}.png"):
    setuplvl()
    xpos,ypos=0,550
  else:
    print("\nYOU WON")
    sys.exit()
    pygame.quit()
  while True:
    setmask()
    draw()
    drawchar()
    touch_lava=touchingmask(lava) #added this already
    touch_jumpy=touchingmask(jumpy) #added
    touch_fastleft=touchingmask(fastleft) #added
    touch_fastright=touchingmask(fastright) #OK
    touch_water=touchingmask(water) #doing this
    touch_shrink=touchingmask(shrink) #ok
    touch_normal=touchingmask(normal)#ok
    touch_win=touchingmask(win) #already did this
    if big:
      up_touch=touchingmask2(top,0,1)
      down_touch=touchingmask2(bottom,0,0)
      side_touch=touchingmask2(side,1,0)
    else:
      up_touch=touchingmask2(topsmall,0,1)
      down_touch=touchingmask2(bottomsmall,0,0)
      side_touch=touchingmask2(sidesmall,1,0)
    if not side_touch:
      if xvel>1:
        xvel-=1
      elif xvel<-1:
        xvel+=1
      else:
        xvel=0
    if not down_touch:
      if not touch_water:
        yvel-=1
      else:
        ypos+=1
    else:
      yvel=0
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP] and down_touch and not touch_water:
      yvel+=20
    if keys[pygame.K_UP] and touch_water:
      ypos-=3
    if keys[pygame.K_LEFT]:
      xvel-=1.5
      if big:
        costume=playerleft
      else:
        costume=playersmallleft
    if keys[pygame.K_RIGHT]:
      xvel+=1.5
      if big:
        costume=playerright
      else:
        costume=playersmallright
    if not big and costume==playerleft:
      costume=playersmallleft
    if not big and costume==playerright:
      costume=playersmallright
    if big and costume==playersmallleft:
      costume=playerleft
    if big and costume==playersmallright:
      costume=playerright
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        pygame.quit()
    if xpos<0:
      xvel=-xvel
      xpos=0
    if xpos>650:
      xvel=-xvel
      xpos=650
    if touch_lava:
      xpos,ypos=0,550
    if side_touch:
      xvel=-xvel
    if up_touch:
      ypos+=1
      yvel=0
    if touch_jumpy:
      yvel+=5
    if touch_fastleft:
      xvel+=3
    if touch_fastright:
      xvel-=3
    if touch_shrink:
      big=False
    if touch_normal:
      big=True
    if touch_water:
      yvel=0
    xpos+=xvel
    ypos-=yvel
    pygame.display.flip()
    if touch_win:
      level+=1
      break
