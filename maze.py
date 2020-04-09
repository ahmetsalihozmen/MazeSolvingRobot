import numpy as np 
import pygame
import time

maze=[]   #Maze will keep the coordinates in the maze
stack=[]    #Stack will be used in the creating maze and while robot tries the find solution
visited=[]  #Visited keeps the places visited by the robot
solution= {} #Solution keeps the shortest way

FPS = 30
WIDTH=500
HEIGHT=600
WHITE=(255,255,255)
RED=(255,0,0)
BLACK=(0,0,0)
w=20

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solving Robot")

class robot():#Robot class keeps the robot direction and position
   def __init__(self,direction,position):
       self.direction=direction
       self.position=position

def buildlines(x,y,w): #This function prints the lines
    for i in range(1,13):
        x = 20                                                            
        y = y + 20                                                       
        for j in range(1,9):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])          
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           
            maze.append((x,y))                                            
            x = x + 20

#These functions removes the walls between the positions
def push_up(x, y):  
    pygame.draw.rect(screen, RED, (x + 1, y - w + 1, 19, 39), 0)         
    pygame.display.update()                                             

def push_down(x, y):
    pygame.draw.rect(screen, RED, (x +  1, y + 1, 19, 39), 0)
    pygame.display.update()

def push_left(x, y):
    pygame.draw.rect(screen, RED, (x - w +1, y +1, 39, 19), 0)
    pygame.display.update()

def push_right(x, y):
    pygame.draw.rect(screen, RED, (x +1, y +1, 39, 19), 0)
    pygame.display.update()

def single_cell( x, y):
    pygame.draw.rect(screen, RED, (x +1, y +1, 18, 18), 0)          
    pygame.display.update()

def robot_cell(x,y,dir):    #These function draws the robot on maze
    if(dir=="S"):
        pygame.draw.rect(screen, WHITE, (x+4, y+4, 12, 12), 0) 
        pygame.draw.rect(screen, BLACK, (x+8, y+12, 5, 5), 0)            
        pygame.display.update() 
    elif(dir=="N"):
        pygame.draw.rect(screen, WHITE, (x+4, y+4, 12, 12), 0) 
        pygame.draw.rect(screen, BLACK, (x+8, y+4, 5, 5), 0)            
        pygame.display.update() 
    elif(dir=="E"):
        pygame.draw.rect(screen, WHITE, (x+4, y+4, 12, 12), 0) 
        pygame.draw.rect(screen, BLACK, (x+12, y+8, 5, 5), 0)            
        pygame.display.update()  
    elif(dir=="W"):
        pygame.draw.rect(screen, WHITE, (x+4, y+4, 12, 12), 0) 
        pygame.draw.rect(screen, BLACK, (x+4, y+8, 5, 5), 0)            
        pygame.display.update()    

def startfinish():  #Function decides which position is start and whic position is finish
    start=np.random.randint(1,9)   
    finish=np.random.randint(1,9)
    start*=20
    finish*=20
    return start,finish
    
def buildmaze(start,finish):   #In this function code creates random maze
    x=start
    y=20
    a=0        
    pygame.display.update()
    visited.append((x,y))   #If position in visited then we will not print that position again
    stack.append((x,y))     #Stack will be used for all position that we draw
    prevdirect="S"
    while len(stack)>0: #While stack is not in the start position we will draw the maze
        celladd=[]
        if (x + w, y) not in visited and (x + w, y) in maze:       
            celladd.append("right")                                 
        if (x - w, y) not in visited and (x - w, y) in maze:      
            celladd.append("left")
        if (x , y + w) not in visited and (x , y + w) in maze:    
            celladd.append("down")
        if (x, y - w) not in visited and (x , y - w) in maze:     
            celladd.append("up")
        if len(celladd) > 0:
            cell = np.random.choice(celladd)
            if cell == "right":                            
                maze.append((x+1,y))
                push_right(x, y)                                  
                solution[(x + w, y)] = x, y ,"E",prevdirect  
                prevdirect="E"                    
                x = x + w             
                maze.append((x-1,y))                            
                visited.append((x, y))                             
                stack.append((x, y))                                
            elif cell == "left":
                maze.append((x-1,y))
                push_left(x, y)
                solution[(x - w, y)] = x, y,"W",prevdirect 
                prevdirect="W"
                x = x - w
                maze.append((x+1,y))
                visited.append((x, y))
                stack.append((x, y))

            elif cell == "down":
                maze.append((x,y+1))
                push_down(x, y)
                solution[(x , y + w)] = x, y,"S",prevdirect 
                prevdirect="S"
                y = y + w
                maze.append((x,y-1))
                visited.append((x, y))
                stack.append((x, y))

            elif cell == "up":
                maze.append((x,y-1))
                push_up(x, y)
                solution[(x , y - w)] = x, y,"N",prevdirect 
                prevdirect="N"
                y = y - w
                maze.append((x,y+1))
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y =stack.pop() 
            single_cell(x,y)
    pygame.draw.rect(screen, (81,0,11), (start +1, 20+1, 18, 18), 0) 
    pygame.draw.rect(screen, (81,0,11), (finish +1, 240+1, 18, 18), 0) 
    pygame.display.update()
        
def solutionway(start,finish): #Function will find the shortest way cost
    i=0
    x=finish
    y=240
    a="c"
    prevdirect="S"
    while(x,y)!=(start,20):
        x,y,direct,prevdirect = solution[x,y]
        if direct!=prevdirect:
            if prevdirect=="N" or prevdirect=="S":
                if direct=="E" or direct=="W":
                    i+=1
        if prevdirect=="E" or prevdirect=="W":
                if direct=="N" or direct=="S":
                    i+=1
        i+=1  
    return i      
               
def robotsolution(robot):  #In this function the robot solves the maze 
    cost=0
    visited=[]
    while robot.position!=(finish,240):
        pygame.draw.rect(screen, (81,0,11), (start +1, 20+1, 18, 18), 0) 
        move=[]
        x=robot.position[0]
        y=robot.position[1]
        robot_cell(robot.position[0],robot.position[1],robot.direction)
        visited.append((robot.position[0],robot.position[1]))
        prevdirect=robot.direction             #Robot will tries to go South than East than West and last North
        if (x,y+1) in maze and robot.direction!="N" and (robot.position[0],robot.position[1]+20) not in visited:
            move.append("S")
        if (x,y-1) in maze and robot.direction!="S" and (robot.position[0],robot.position[1]-20) not in visited:
            move.append("N")
        if (x+1,y) in maze and robot.direction!="W" and (robot.position[0]+20,robot.position[1]) not in visited:
            move.append("E")
        if (x-1,y) in maze and robot.direction!="E" and (robot.position[0]-20,robot.position[1]) not in visited:
            move.append("W")
        
        if "S" in move: #Due to the next position we will push the current position in stack and print the robot on the next position
            robot_cell(robot.position[0],robot.position[1],"S")
            stack.append("N")
            stack.append((robot.position[0],robot.position[1]))
            time.sleep(.1)
            single_cell(robot.position[0],robot.position[1])
            robot.position=(robot.position[0],robot.position[1]+20)
            robot.direction="S"
            robot_cell(robot.position[0],robot.position[1],"S")   
            time.sleep(.1)
            if prevdirect!=robot.direction: #Increasing the cost
                  cost+=1
            cost+=1
        elif "E" in move:
            robot_cell(robot.position[0],robot.position[1],"E")
            stack.append("W")
            stack.append((robot.position[0],robot.position[1]))
            time.sleep(.1)
            single_cell(robot.position[0],robot.position[1])
            robot.position=(robot.position[0]+20,robot.position[1])
            robot.direction="E"
            robot_cell(robot.position[0],robot.position[1],"E")   
            time.sleep(.1)
            if prevdirect!=robot.direction:
                  cost+=1
            cost+=1  
        elif "W" in move:
            robot_cell(robot.position[0],robot.position[1],"W")
            stack.append("E")
            stack.append((robot.position[0],robot.position[1]))
            time.sleep(.1)
            single_cell(robot.position[0],robot.position[1])
            robot.position=(robot.position[0]-20,robot.position[1])
            robot.direction="W"
            robot_cell(robot.position[0],robot.position[1],"W")
            time.sleep(.1)
            if prevdirect!=robot.direction:
                  cost+=1
            cost+=1
        elif "N" in move:
            robot_cell(robot.position[0],robot.position[1],"N")
            stack.append("S")
            stack.append((robot.position[0],robot.position[1]))
            time.sleep(.1)
            single_cell(robot.position[0],robot.position[1])
            robot.position=(robot.position[0],robot.position[1]-20)
            robot.direction="N"
            robot_cell(robot.position[0],robot.position[1],"N") 
            time.sleep(.1)
            if prevdirect!=robot.direction:
                  cost+=1
            cost+=1
            
        if(len(move)==0):   #If robot is stuck than robot will go the previous position
            single_cell(robot.position[0],robot.position[1])
            prevpos=robot.position
            robot.position=stack.pop()  #Robot will take previous position and direction from stack
            robot.direction=stack.pop()
            if prevdirect==robot.direction:
                robot_cell(robot.position[0],robot.position[1],robot.direction)
            elif robot.direction=="N":
                 if prevdirect=="W":
                     robot_cell(prevpos[0],prevpos[1],"N")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                 else:
                     robot_cell(prevpos[0],prevpos[1],"E")
                     time.sleep(.1)
                     robot_cell(prevpos[0],prevpos[1],"N")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                     if prevdirect=="S":
                         cost+=2
                     else:
                         cost+=1 
            elif robot.direction=="S":
                 if prevdirect=="W":
                     robot_cell(prevpos[0],prevpos[1],"S")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                 else:
                     robot_cell(prevpos[0],prevpos[1],"E")
                     time.sleep(.1)
                     robot_cell(prevpos[0],prevpos[1],"S")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                     if prevdirect=="N":
                         cost+=2
                     else:
                         cost+=1 
            elif robot.direction=="E":
                 if prevdirect=="N":
                     robot_cell(prevpos[0],prevpos[1],"N")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                 else:
                     robot_cell(prevpos[0],prevpos[1],"S")
                     time.sleep(.1)
                     robot_cell(prevpos[0],prevpos[1],"E")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1) 
                     if prevdirect=="W":
                         cost+=2
                     else:
                         cost+=1          
            elif robot.direction=="W":
                 if prevdirect=="N":
                     robot_cell(prevpos[0],prevpos[1],"W")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                     cost+=1
                 else:
                     robot_cell(prevpos[0],prevpos[1],"S")
                     time.sleep(.1)
                     robot_cell(prevpos[0],prevpos[1],"W")
                     time.sleep(.1)
                     single_cell(prevpos[0],prevpos[1])
                     robot_cell(robot.position[0],robot.position[1],robot.direction)
                     time.sleep(.1)
                     if prevdirect=="E":
                         cost+=2
                     else:
                         cost+=1 
            cost+=1                
    robot_cell(robot.position[0],robot.position[1],"S")   
    time.sleep(.1) 
    return cost     
                  
buildlines(0, 0, 20) #Building the lines
pygame.display.update()
start,finish=startfinish() #Make the start and finish position
buildmaze(start,finish)
way=solutionway(start,finish)
robot1 = robot("S",(start,20)) #Giving the robot start position
rcost=robotsolution(robot1)
print("Shortest way cost is="+str(way))
print("Robot cost is="+str(rcost))
input(w)

