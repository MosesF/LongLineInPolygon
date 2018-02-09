import matplotlib.pyplot as plt
import math

"""
incline Function
takes in a coordinate and finds it's incline from 0-360 from the origin (0, 0)
"""


def incline(a1, b1):
    # Calculates incline in radians
    a = math.atan2(b1, a1)
    #converts to degrees
    a = math.degrees(a)
    # '%' converts incline from '-180 - 180' to '0 - 360'
    a = a % 360
    return a


"""
Sweep Function

Sweep Function takes in coordinates:

Endpoint, Origin, Previous Neighbor, and Next Neighbour

It checks the incline created by the origin and it's neighbours to determine

if the vector created from origin to endpoint lies within the range

This is used to check if the line created from a vertex will be inside the final shape

**ONLY WORKS WHEN COORDINATES ARE INPUTTED IN COUNTER-CLOCKWISE ORDER
"""


def sweep_fcn(a2, b2, c2, d2):
    # by subtracting the origins x & y coordinates from the neighbours it moves the vector's tail to the true origin
    in1 = incline((c2[0] - b2[0]), (c2[1] - b2[1]))
    in2 = incline((d2[0] - b2[0]), (d2[1] - b2[1]))
    inc = incline((a2[0] - b2[0]), (a2[1] - b2[1]))

    # if the previous incline is greater than the next incline, the line must be in range of the inclines to be in the shape**
    if in1 > in2:
        return in_range(inc, in2, in1, True)
    # if the previous incline is less than the next incline,
    # the line must not be in range of the two inclines to be in the shape**
    else:
        return not in_range(inc, in2, in1, True)


"""
In Range Function

In range checks the value of x to see if it lies between y and z

inclusive boolean determines whether or not to include a value of y and z as in range
"""


def in_range(x1, y1, z1, inclusive):
    if (inclusive):
        # after the larger of y1 and z1 is found x1 is checked if it is in range
        if ((y1 <= z1) and (y1 <= round(x1, 4) <= z1)):
            return True
        elif ((z1 <= y1) and (z1 <= round(x1, 4) <= y1)):
            return True
        else:
            return False
    else:
        if ((y1 < z1) and (y1 < round(x1, 4) < z1)):
            return True
        elif ((z1 < y1) and (z1 < round(x1, 4) < y1)):
            return True
        else:
            return False

"""
Get Length Function

Get length uses pythagoras' theorem on two coordinates to determine the distance between the two
"""


def get_length(p1, p2):
    len = math.sqrt(abs(p1[1] - p2[1]) ** 2 + abs(p1[0] - p2[0]) ** 2)
    return len

"""
Line Function

Line function takes in two coordinates an finds the point-slope formula

returns as a tuple of (slope, offset)
"""

def line(p3, p4):
    #If the X value is the same of both coordinates, slope is infinite
    if (p3[0] == p4[0]):
        m = math.inf
    else:
        #Slope is calculated by delta y over delta x
        m = (p4[1] - p3[1]) / (p4[0] - p3[0])
    # b is solved by re-arranging y = mx + b
    b = p4[1] - p4[0] * m
    mb = (m, b)
    return mb

"""
Intercept Function

Intercept takes in two lines' slope and offset to determine at what point they intersect
"""
def intercept(m1, b1, m2, b2):
    #If the slopes are equal the two lines will not intersect
    if (m1 == m2):
        return 0

    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1
    return (x, y)

"""
Intercept Line-Segment Function

Determines if an infinite line and a segment will intersect and if so, at what coordinate

p1 and p2 are the endpoints of the segment, lin is the line
"""
def intercept_LS(p1, p2, lin):

    # Finds the slope and offset of the segment
    ln = line(p1, p2)

    #Stores slope and offset of lin in variables
    m = lin[0]
    b    = lin[1]

    # if the slope of the intercept is infinite it must do a special check
    if (ln[0] == math.inf):

        #The y-coordinate of lin is found at the x of the segment, (since the slope is infinite there is only one x for all y)
        y = m * p1[0] + b

        #If the y-coordinate is within the endpoints of the segment then there is an intersection at x, y
        if (in_range(y, p1[1], p2[1], False)):
            return (p1[0], (m * p1[0] + b))
        else:
            return 0

    # if the slope is not infinite the function checks for the intercept of the line and the segment as if the segment was a line
    ipt = intercept(ln[0], ln[1], m, b)

    if (ipt):
        #If there is an intersection it checks to see if the x-coordinates falls between the endpoints
        if (in_range(ipt[0], p1[0], p2[0], False)):
            return (ipt[0], ipt[1])
        else:
            return 0
    else:
        return 0

#coord will hold of the the vertices in a counter clockwise order
coord = []
#First the number of inputs is stated
m = input()

#Then each coordinate in the list is added to the array
for i in range(0, int(m)):
    #Map will get both the x and y values as integers from txt separated by spaces
    x, y = map(int, input().split())
    #the new coordinate (x, y) is appended into coord
    coord.append((x, y))

#Plot axes is initialized
plt.axes()
#A shape is created with the coordinated from coord with no fill and a blue colour
shape = plt.Polygon(coord, fill=None, edgecolor='b')
# The shape is added to the axes
plt.gca().add_patch(shape)

#The current longest line found is 0 since no lines have been found, it's endpoints are set to the origin
longest = 0
lStart = (0, 0)
lEnd = (0, 0)
#coord[i] represents the beginning of the line on a vertex, it cycles through all of the vertices in order
for i in range(-1, len(coord) - 1):
    #coord[j] will be used to find the slope between two vertices, it will loop from i+1 to the end to ensure no pair gets checked twice
    for j in range(i + 1, len(coord)):
        #The origin point will be the point the line centres around
        origin = coord[i]

        #Above is a boolean to determine if the line has collided with an edge above the origin
        Above = True
        #clipC will be the intercept coordinate on the first edge the line hits in the positive y direction, it is called the ceiling
        clipC = 0
        #Below is a boolean to determine if the line has collided with an edge below the origin
        Below = True
        # clipF will be the intercept coordinate on the first edge the line hits in the negative y direction, it is called the floor
        clipF = 0

        #Sweep is used to see if the line being drawn falls within the area of the shape, if it does not it will not be checked
        if (sweep_fcn(coord[j], coord[i], coord[i - 1], coord[i + 1])):
            #coord[k] and coord[k+1] are the endpoints of the edges of the shape, k begins at -1 which is the last point of the object
            #this prevents an out of bound error when the last coordinate is checked with k+1
            for k in range(-1, len(coord) - 1):
                #The line is checked to see if it collides with an edge
                intc = intercept_LS(coord[k], coord[k + 1], line(coord[i], coord[j]))
                if (intc):
                    #If the intersection is above the origin and no ceiling has been found it becomes the ceiling
                    if (not clipC and (intc[1] > origin[1])):
                        #Above is set to false meaning a ceiling has been found
                        Above = False
                        clipC = intc
                    #If a new ceiling is found that is lower than the current one it will become the new ceiling
                    #This means it is the first edge that is hit in the positive y direction
                    elif (clipC and origin[1] < intc[1] < clipC[1]):
                        clipC = intc
                    #Checks are done for intercepts below the origin to find the floor
                    if (not clipF and (intc[1] < origin[1])):
                        Below = False
                        clipF = intc
                    elif (clipF and clipF[1] < intc[1] < origin[1]):
                        clipF = intc

            if (Above):
                #if no ceiling was found the higher coordinate between coord[i] and [j] becomes the ceiling
                if (coord[i][1] > coord[j][1]):
                    clipC = coord[i]
                else:
                    clipC = coord[j]
            if (Below):
                # if no floor was found the lower coordinate between coord[i] and [j] becomes the floor
                if (coord[i][1] > coord[j][1]):
                    clipF = coord[j]
                else:
                    clipF = coord[i]
            #The final length of the line is the distance between the ceiling coordinate and the floor coordinate
            currLength = get_length(clipF, clipC)

            #If the line checked is longer than the current longest, it becomes the new longest and the endpoints are saved as lStart and lEnd
            if (currLength > longest):
                longest = currLength
                lStart = clipF
                lEnd = clipC

# The information of the longest line is printed
print('Longest line is:', lStart, '--', lEnd, '@', longest)

#A line is created from the beggining and end points and coloured red
co = (lStart, lEnd)
longLine = plt.Polygon(co, closed=None, color='r')

#it is added to the axes
plt.gca().add_patch(longLine)

#The axis is scaled to view the full shape and the window is displayed
plt.axis('scaled')
plt.show()
