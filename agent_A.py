import random
import time

random.seed(time.time())

# we decided to create object and properties for the rooms and the robot.
class Rooms:    
    def __init__(self,room, state, probabilty, operations):
        self.room = room                        # this indicates which room is. (room A, room B ,room C)
        self.state = state                      # this indicates whether the room is C (clean) or D (dirty)
        self.probabilty = probabilty            # the rooms have different probabilities. So each room object holds probability seperately
        self.operations = operations            # the rooms have different operations such as, if current room is a, the robot can't go left so right, noOp and suck operations available.

class Robot:
    def __init__(self, location, total_point, isDirty_A, isDirty_B, isDirty_C):
        self.location = location                # this property indicates the current location of robot.
        self.total_point = total_point          # this property holds the total point gained
        self.isDirty_A = isDirty_A
        self.isDirty_B = isDirty_B
        self.isDirty_C = isDirty_C

# this function finds the largest probability when called.
def find_largest_prob(a, b, c):
    if a > b and a > c:
        return a
    elif c > a and c > b:
        return c
    else:
        return b

# # User will enter the probability of rooms get dirty.
Pa = float(input("Pa = "))
Pb = float(input("Pb = "))
Pc = float(input("Pc = "))


#creating files for each simulation.
f = open("a_5_09.txt", "a")

# We decided to hold each count (increments when suck at room X [x is one of A or B or C]), total (increments when the X room visited [x is one of A or B or C]) values specific to room.
# The reason is, when the agent tries to learn the probabilities of getting dirty for a specific room, It counts the visited time of that room and also counts the suck operations for that room.
# The division of count / total will give an approximation of probabilities.
countA = 0
totalA = 0

countB = 0
totalB = 0

countC = 0
totalC = 0

# We decided to hold the priority informations for each room. The reason is, when we try to choose the rooms according to bigger dirty probabilities, usually "camping" (staying same room) occurs. 
# If we stay on same room some time, also we increase the priority of other rooms.
priority_A = 0.0
priority_B = 0.0
priority_C = 0.0

# Initializing rooms (room name, state, probability of gets dirty, operations[])
a = Rooms("A", "D", Pa, ["Right", "noOp"])
b = Rooms("B", "D", Pb, ["Left", "Right", "noOp"])
c = Rooms("C", "D", Pc, ["Left", "noOp"])

# Initializing robot at b and 0 total points. Initially, robot assumes 0.5 each room probabilty.
robot = Robot(b , 0, 0.5, 0.5, 0.5)


j = 1
while j < 1001:    
    # print(f"Step {j}")
    # print(f"{(robot.location).room}, {a.state}, {b.state}, {c.state}")
    
    f.write(f"Step {j}\n")
    f.write(f"{(robot.location).room}, {a.state}, {b.state}, {c.state}\n")
    
    # In each 100 iteration, the estimated probabilities of A (Pa), B (Pb), C (Pc)  calculated again.
    # According to comparison Pa, Pb, Pc with isDirtyA / B / C (holds the current probability of rooms getting dirty)
    # the new probability determined.
    if(j % 100 == 0):    
        est_Pa = round((countA / totalA), 1)
        est_Pb = round((countB / totalB), 1)
        est_Pc = round((countC / totalC), 1)        

        if(est_Pa > robot.isDirty_A):
            robot.isDirty_A += 0.1
            robot.isDirty_A = round(robot.isDirty_A,1)
        elif(est_Pa < robot.isDirty_A):
            robot.isDirty_A -= 0.1
            robot.isDirty_A = round(robot.isDirty_A,1)
        else:
            robot.isDirty_A = est_Pa
            robot.isDirty_A = round(robot.isDirty_A,1)


        if(est_Pb > robot.isDirty_B):
            robot.isDirty_B += 0.1
            robot.isDirty_B = round(robot.isDirty_B,1)
        elif(est_Pb < robot.isDirty_B):
            robot.isDirty_B -= 0.1
            robot.isDirty_B = round(robot.isDirty_B,1)
        else:
            robot.isDirty_B = est_Pb
            robot.isDirty_B = round(robot.isDirty_B,1)
            
    
        if(est_Pc > robot.isDirty_C):
            robot.isDirty_C += 0.1
            robot.isDirty_C = round(robot.isDirty_C,1)
        elif(est_Pc < robot.isDirty_C):
            robot.isDirty_C -= 0.1
            robot.isDirty_C = round(robot.isDirty_C,1)
        else:
            robot.isDirty_C = est_Pc
            robot.isDirty_C = round(robot.isDirty_C,1)
        
        
        # According to new calculated isDirty variables, new main room ( dirty_room ) selected.
        max = find_largest_prob(robot.isDirty_A, robot.isDirty_B, robot.isDirty_C)
        if(max == robot.isDirty_B):
            dirty_room = b.room
        elif(max == robot.isDirty_A):
            dirty_room = a.room
        else:
            dirty_room = c.room


    # Counting how many times we visited each room seperately.
    if((robot.location).room == a.room):
        totalA += 1
    elif ((robot.location).room == b.room):
        totalB += 1
    else:
        totalC += 1
    
    # In this if block, if the room is dirty, Suck operation performed and gained 1 point.    
    if((robot.location).state == "D"):
        if((robot.location).room == a.room):
            countA +=1
        elif((robot.location).room == b.room):
            countB +=1
        else:
            countC +=1

        # print("suck")
        f.write("suck\n")
        robot.total_point += 1
        (robot.location).state = "C"

    else:
        # need to decide which operation will be performed.
        if(j > 100):
  
            if((robot.location).room == b.room):
                # if robot located one of the room, the other rooms priority increases by its probability according to the robot.
                priority_B = 0
                priority_A += robot.isDirty_A
                priority_C += robot.isDirty_C
                
                if(priority_C >= 1.0):
                    robot.location = c
                    # print("Right")
                    f.write("Right\n")
                elif (priority_A >= 1.0):
                    robot.location = a
                    # print("Left")
                    f.write("Left\n")
                else:
                    if(dirty_room == a.room):
                        robot.location = a
                        # print("Left")
                        f.write("Left\n")
                    elif (dirty_room == c.room):
                        robot.location = c
                        # print("Right")
                        f.write("Right\n")
                    else:
                        # print("noOp")
                        f.write("noOp\n")
                        robot.location = b
            
            elif((robot.location).room == a.room):
                priority_A = 0
                priority_B += robot.isDirty_B
                priority_C += robot.isDirty_C
                
                if(priority_B >= 1.0):
                    robot.location = b
                    # print("Right")
                    f.write("Right\n")
                else:
                    if(dirty_room == b.room or dirty_room == c.room ):
                        robot.location = b
                        # print("Right")
                        f.write("Right\n")
                    else:
                        # print("noOp")
                        f.write("noOp\n")
                        robot.location = a
            
            else:
                priority_C = 0
                priority_B += robot.isDirty_B
                priority_A += robot.isDirty_A
                
                if(priority_B >= 1.0): ## 1.5 yap, harekette -0.5
                    robot.location = b
                    # print("Left")
                    f.write("Left\n")
                else:
                    if(dirty_room == b.room or dirty_room == a.room ):
                        robot.location = b
                        # print("Left")
                        f.write("Left\n")
                    else:
                        # print("noOp")
                        f.write("noOp\n")
                        robot.location = c

        # In this else block, we calculate first estimations of Pa, Pb, Pc
        # To do this, the robot will randomly go between A, B or C.    
        else: 
            random_op = random.choice((robot.location).operations)
            # print(random_op)
            f.write(f"{random_op}\n")
            if(random_op == "Left"):
                if((robot.location).room == "B"):
                    robot.location = a
                else:
                    robot.location = b
            
            elif(random_op == "Right"):

                if((robot.location).room == "A"):
                    robot.location = b
                else:
                    robot.location = c

    # print(f"{(robot.location).room}, {a.state}, {b.state}, {c.state}") 
    # print(f"{robot.total_point}")   
    
    f.write(f"{(robot.location).room}, {a.state}, {b.state}, {c.state}\n")
    f.write(f"{robot.total_point}\n")
    
    # In this part, the next state of rooms determined.
    y = random.random()
    if(a.state == "C"):
        if(a.probabilty >= y):
            a.state = "D"
    
    if(b.state == "C"):
        if(b.probabilty >= y):
            b.state = "D"
    
    if(c.state == "C"):
        if(c.probabilty >= y):
            c.state = "D"
    j += 1    
    # print("\n")
    f.write("\n")

# print(f" Pa ={Pa}\n est_Pa= {est_Pa}\n robot_isDirty_a ={robot.isDirty_A}\n Pb ={Pb}\n est_Pb ={est_Pb}\n isDirty_b {robot.isDirty_B}\n Pc ={Pc}\n est_Pc {est_Pc}\n isDirty_C {robot.isDirty_C}")
# print(f"Total point {robot.total_point}")
f.write(f"Total point : {robot.total_point}\n")

f.close