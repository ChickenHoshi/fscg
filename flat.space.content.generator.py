import pygame, sys, math, time
from time import strftime
from pygame.locals import*

pygame.init()
FPS = 25
fpsClock = pygame.time.Clock()
#set up window
windowX = 1080
windowY = 720
DISPLAYSURF = pygame.display.set_mode((windowX,windowY))
previewSurface  = pygame.Surface((windowX*2, windowY*2))
pygame.display.set_caption('FSCG')
font = pygame.font.SysFont('consolas',20)
modes = ['line','box','circle', '::setCenter::','preview','free poly - open (TODO)',
         'free poly - closed (TODO)','dot (TODO)']
lines = []
circles = []
quads = []

linesPreview = False
circlesPreview = [False]
quadsPreview = [False]

rotationCenter = [False]
#set up colors
def findAngle(x,y,pos):
     opp, adj = -(pos[1] - y), (pos[0] - x)
     if adj == 0: adj = -1
     deg = math.degrees(math.atan(opp/adj))
     if x < pos[0]:
          deg += 180
     return deg



def makeLine():
     if start['line'] == False:
          lines.append([])
          lines[-1].append([mposX,mposY])
          start['line'] = True
     else:
          lines[-1].append([mposX,mposY])
          start['line'] = False

          
def makeCircle():
     if start['circle'] == False:
          circles.append([])
          circles[-1].append([mposX,mposY])
          start['circle'] = True
     else:
          rad = int(abs(math.hypot(mposX - circles[-1][0][0],mposY - circles[-1][0][1])))
          circles[-1].append(rad)
          start['circle'] = False

def makeBox():
     if start['quad'] == 0:
          quads.append([])
          quads[-1].append([mposX,mposY])
          start['quad'] = 1
     elif start['quad'] == 1:
          quads[-1].append([mposX, quads[-1][-1][1]])
          quads[-1].append([quads[-1][-1][0], mposY])
          quads[-1].append([quads[-1][0][0], quads[-1][-1][1]])
          start['quad'] = 2     
     else:
          center = (int((quads[-1][0][0] + quads[-1][1][0])/2), int((quads[-1][0][1] + quads[-1][2][1])/2))
          angle = findAngle(mposX,mposY,center)
          rad = math.hypot(center[0] - quads[-1][0][0], center[1] - quads[-1][0][1])
          for i in range(4):
               angle0 = findAngle(quads[-1][i][0],quads[-1][i][1],center)
               quads[-1][i][0] = int(center[0] + rad* math.cos(math.radians(angle0 + angle)))
               quads[-1][i][1] = int(center[1] - rad* math.sin(math.radians(angle0 + angle)))
          start['quad'] = 0
          

def drawGrid(res):
     color = (200,200,200)
     for i in range(0,windowX,res):
          pygame.draw.line(DISPLAYSURF,color,(i,0),(i,windowY))
     for i in range(0,windowY,res):
          pygame.draw.line(DISPLAYSURF,color,(0,i),(windowX,i))


def setCenter():
     rotationCenter[0] = (mposX, mposY)
     
##     if start['
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
mode = 0
time = 0
center, rad = -1, -1
start = {'line' : False, 'circle' : False, 'quad' : 0, 'center' : False}
res = [True,10]
while True: ##main game loop
     if time < 1200: time += 1
     else: time = 0
     #get mouse position
     mposX, mposY = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
     if res[0]:
          mposX += int(res[1]/2 - mposX%res[1])
          mposY += int(res[1]/2 - mposY%res[1])
     
     DISPLAYSURF.fill(WHITE)
     drawGrid(res[1])

     
     currentMode = font.render(modes[mode],1,BLACK)
     DISPLAYSURF.blit(currentMode,(0,0))


     
     if modes[mode] != 'preview':
          #draw all lines
          if start['line'] == False:
               for i in range(len(lines)):
                    pygame.draw.aaline(DISPLAYSURF,BLACK,lines[i][0],lines[i][1])
          else:
               for i in range(len(lines)-1):
                    pygame.draw.aaline(DISPLAYSURF,BLACK,lines[i][0],lines[i][1])
          if start['line']:
               pygame.draw.line(DISPLAYSURF,BLACK,lines[-1][0],(mposX,mposY))

          #draw all circles
          if start['circle'] == False:
               for i in range(len(circles)):
                    pygame.draw.circle(DISPLAYSURF,BLACK,circles[i][0],circles[i][1],1)
          else:
               for i in range(len(circles)-1):
                    pygame.draw.circle(DISPLAYSURF,BLACK,circles[i][0],circles[i][1],1)
          if start['circle']:
               rad = int(abs(math.hypot(mposX - circles[-1][0][0],mposY - circles[-1][0][1])))
               if rad < 1: rad = 1
               pygame.draw.circle(DISPLAYSURF,BLACK,circles[-1][0],rad,1)

          #draw all boxes
          
          if start['quad'] == 0:
               for i in range(len(quads)):
                    pygame.draw.polygon(DISPLAYSURF,BLACK,quads[i],1)
          else:
               for i in range(len(quads)-1):
                    pygame.draw.polygon(DISPLAYSURF,BLACK,quads[i],1)
          if start['quad'] == 1:
               p1 = [mposX, quads[-1][-1][1]]
               p2 = [mposX, mposY]
               p3 = [quads[-1][-1][0], mposY]
               pygame.draw.polygon(DISPLAYSURF, BLACK,([quads[-1][-1][0],quads[-1][-1][1]],p1, p2, p3),1)
               center = (int((quads[-1][0][0] + p1[0])/2), int((quads[-1][0][1] + p2[1])/2))
               rad = math.hypot(center[0] - quads[-1][0][0], center[1] - quads[-1][0][1])
          if start['quad'] == 2:
               box_draw_temp = []
               angle = findAngle(mposX,mposY,center)
               for i in range(4):
                    angle0 = findAngle(quads[-1][i][0],quads[-1][i][1],center)
                    qx = int(center[0] + rad* math.cos(math.radians(angle0 + angle)))
                    qy = int(center[1] - rad* math.sin(math.radians(angle0 + angle)))
                    box_draw_temp.append((qx,qy))
               pygame.draw.polygon(DISPLAYSURF, BLACK,box_draw_temp,1)
          if modes[mode] == '::setCenter::':
               #setCenter()
               color = (255,0,0)
               pygame.draw.line(DISPLAYSURF,color,(mposX,0),(mposX, windowY))
               pygame.draw.line(DISPLAYSURF,color,(0,mposY),(windowX, mposY))
               pygame.draw.circle(DISPLAYSURF,color,(mposX,mposY),5,1)
               
          if rotationCenter[0] != False:
               pygame.draw.circle(DISPLAYSURF,(255,0,255),rotationCenter[0],5,1)

     if modes[mode] == 'preview':
          previewSurface.fill(WHITE)
          
        
          if rotationCenter[0] != False:
               cx = rotationCenter[0][0] + windowX/4
               cy = rotationCenter[0][1] + windowY/4
               for circle in circles:
                    rad = math.hypot(rotationCenter[0][0] - circle[0][0], rotationCenter[0][1] - circle[0][1])
                    angle0 = findAngle(circle[0][0],circle[0][1], rotationCenter[0])
                    px = cx + rad* math.cos(math.radians(angle0 + time))
                    py = cy - rad* math.sin(math.radians(angle0 + time))
                    pygame.draw.circle(previewSurface,BLACK,(int(px),int(py)),circle[1],1)

                    
               for line in lines:
                    prevwLine = []
                    for pos in line:
                         rad = math.hypot(rotationCenter[0][0] - pos[0], rotationCenter[0][1] - pos[1])
                         angle0 = findAngle(pos[0],pos[1], rotationCenter[0])
                         prevwLine.append([])
                         px = cx + rad* math.cos(math.radians(angle0 + time))
                         py = cy - rad* math.sin(math.radians(angle0 + time))
                         prevwLine[-1] = (int(px),int(py))
                    pygame.draw.line(previewSurface,BLACK,prevwLine[0], prevwLine[1])
               for quad in quads:
                    prevwQuad = []
                    for pos in quad:
                         rad = math.hypot(rotationCenter[0][0] - pos[0], rotationCenter[0][1] - pos[1])
                         angle0 = findAngle(pos[0],pos[1], rotationCenter[0])
                         prevwQuad.append([])
                         px = cx + rad* math.cos(math.radians(angle0 + time))
                         py = cy - rad* math.sin(math.radians(angle0 + time))
                         prevwQuad[-1] = (int(px),int(py))
                    pygame.draw.polygon(previewSurface,BLACK,prevwQuad,1)
          DISPLAYSURF.blit(previewSurface, (-int(windowX/4),-int(windowY/4)))           
                    
               
          
          
     for event in pygame.event.get():
          if event.type == MOUSEBUTTONDOWN:
               if event.button == 1:
                    if modes[mode] == 'line': makeLine()
                    if modes[mode] == 'circle': makeCircle()
                    if modes[mode] == 'box': makeBox()
                    if modes[mode] == '::setCenter::': setCenter()
                    
               if event.button == 3:
                    if mode < len(modes)-1: mode += 1
                         
                    else: mode = 0
          if event.type == KEYDOWN:
               if event.key == K_p:
                    if res[0]:res[0] = False
                    else: res[0] = True
               if event.key == K_c:
                    if start['line'] == False and start['circle'] == False and \
                       start['quad'] == 0  and modes[mode] != 'preview':
                         lines = []
                         circles = []
                         quads = []
               if event.key == K_m:
                    if rotationCenter[0] != False:
                         name = 'FSCG '+strftime("%Y-%m-%d %H.%M.%S.txt")
                         file = open(name,'w')
                         file.write("#this works in the format used in my 'flat space' game\n\n\n")
                    
                         for line in lines:
                              for pos in line:
                                   rad = str(math.hypot(rotationCenter[0][0] - pos[0], rotationCenter[0][1] - pos[1]))
                                   angle0 = str(int(findAngle(pos[0],pos[1], rotationCenter[0])))
                                   file.write('[int(self.x + self.rad*math.cos(math.radians(self.angle + ('+angle0+')))),\n'+
                                              'int(self.y - self.rad*math.sin(math.radians(self.angle + ('+angle0+'))))] #self.rad: '+rad+'\n\n')
                         for quad in quads:
                              file.write('[')
                              for pos in quad:
                                   rad = str(math.hypot(rotationCenter[0][0] - pos[0], rotationCenter[0][1] - pos[1]))
                                   angle0 = str(int(findAngle(pos[0],pos[1], rotationCenter[0])))
                                   file.write('[int(self.x + self.rad*math.cos(math.radians(self.angle + ('+angle0+')))),\n'+
                                              'int(self.y - self.rad*math.sin(math.radians(self.angle + ('+angle0+'))))] #self.rad: '+rad+'\n')
                              file.write('] # a rectangle\n\n')
                         for circle in circles:
                              rad = str(math.hypot(rotationCenter[0][0] - circle[0][0], rotationCenter[0][1] - circle[0][1]))
                              angle0 = str(int(findAngle(circle[0][0],circle[0][1], rotationCenter[0])))
                              file.write('[int(self.x + self.rad*math.cos(math.radians(self.angle + ('+angle0+')))),\n'+
                                         'int(self.y - self.rad*math.sin(math.radians(self.angle + ('+angle0+'))))] # radius: '+str(circle[1])+'#self.rad: '+rad+'\n\n')
                         file.close()
                         
                    
          if event.type == QUIT:
               pygame.quit()
               sys.exit()
     pygame.display.update()
     fpsClock.tick(FPS)
