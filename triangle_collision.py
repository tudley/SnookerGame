import math
import pygame
import sys
from time import sleep
import random as ran

"""
pygame.init()
screen = pygame.display.set_mode((700, 700))
tri_colour = (255, 0, 0)
tri1_colour = (0, 0, 0)
bg_colour = (255, 255, 255)
ball_colour = (0, 255, 0)
collision_colour = (0, 0, 255)

class Triangle():
    def __init__(self, x1, y1, x2, y2, x3, y3, colour, screen):
        #x3 and y3 are the edges of the triangle we never touch
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.triangle = ((x1, y1), (x2, y2), (x3, y3))
        self.colour = colour
        self.screen = screen

    def draw_triangle(self):
        pygame.draw.polygon(self.screen, self.colour, self.triangle)

class Circle():
    def __init__(self, cx, cy, r, screen, colour):
        #self.centerx = 
        self.cx = cx
        self.cy = cy
        self.r = r
        self.screen = screen
        self.colour = colour
        self.x_vel = ran.uniform(-2, 2)
        self.y_vel = ran.uniform(-2, 2)
        self.phi = math.pi / 4

        self.tl = (self.cx - self.r * math.sin(self.phi), self.cy - self.r * math.sin(self.phi))
        self.tr = (self.cx + self.r * math.sin(self.phi), self.cy - self.r * math.sin(self.phi))
        self.bl = (self.cx - self.r * math.sin(self.phi), self.cy + self.r * math.sin(self.phi))
        self.br = (self.cx + self.r * math.sin(self.phi), self.cy + self.r * math.sin(self.phi))

        self.corners = {'tl': self.tl, 'tr' : self.tr, 'bl' : self.br, 'br' : self.br}

    
    def draw_circle(self):
        pygame.draw.circle(self.screen, self.colour, (self.cx ,self.cy), self.r)
    
    def update(self):
        #update centerx, y
        self.cx += self.x_vel
        self.cy += self.y_vel

        #update the corner coordinates
        self.tl = (self.cx - self.r * math.sin(self.phi), self.cy - self.r * math.sin(self.phi))
        self.tr = (self.cx + self.r * math.sin(self.phi), self.cy - self.r * math.sin(self.phi))
        self.bl = (self.cx - self.r * math.sin(self.phi), self.cy + self.r * math.sin(self.phi))
        self.br = (self.cx + self.r * math.sin(self.phi), self.cy + self.r * math.sin(self.phi))

        #update the corner dictionary
        self.corners['tl'] = self.tl
        self.corners['tr'] = self.tr
        self.corners['bl'] = self.bl
        self.corners['br'] = self.br

"""

def find_area_of_triangle(triangle):
    """use herons formula to calculate the area of the triangle the ball is bouncing off"""
    # area = root(s * (s - a) * (s- b) * (s - c)) where a, b and  are the lengths of the sides and s is half the perimiter
    #here I use the notation a12, a13 and a23 to indicate which length i am calculating
    a12 = math.sqrt((triangle.x2 - triangle.x1)**2 + (triangle.y2 - triangle.y1)**2)
    a13 = math.sqrt((triangle.x3 - triangle.x1)**2 + (triangle.y3 - triangle.y1)**2)
    a23 = math.sqrt((triangle.x3 - triangle.x2)**2 + (triangle.y3 - triangle.y2)**2)
    s = (a12 + a13 + a23)/2
    area = math.sqrt(s * (s - a12) * (s - a13) * (s - a23))
    return area

def sum_of_areas_between_circle_and_triangle(circle, triangle):
    """find the area of each triangles made by using 2 points on the original triangle, and the center of the ball"""

    list_of_sum_of_areas = []
    for corner in circle.corners.values():
        
        #triangle 12c, using points 1, 2 and c
        a12 = math.sqrt((triangle.x2 - triangle.x1)**2 + (triangle.y2 - triangle.y1)**2)
        a1c = math.sqrt((corner[0] - triangle.x1)**2 + (corner[1] - triangle.y1)**2)
        a2c = math.sqrt((corner[0] - triangle.x2)**2 + (corner[1] - triangle.y2)**2)
        s_12c = (a12 + a1c + a2c)/2
        area_12c = math.sqrt(s_12c * (s_12c - a12) * (s_12c - a1c) * (s_12c - a2c))

        #triangle 23c, using  points 2, 3,and c
        a23 = math.sqrt((triangle.x3 - triangle.x2)**2 + (triangle.y3 - triangle.y2)**2)
        a2c = math.sqrt((corner[0] - triangle.x2)**2 + (corner[1] - triangle.y2)**2)
        a3c = math.sqrt((corner[0] - triangle.x3)**2 + (corner[1] - triangle.y3)**2)
        s_23c = (a23 + a2c + a3c)/2
        area_23c = math.sqrt(s_23c * (s_23c - a23) * (s_23c - a2c) * (s_23c - a3c))

        #triangle 13c, using points 1, 3 and c
        a13 = math.sqrt((triangle.x3 - triangle.x1)**2 + (triangle.y3 - triangle.y1)**2)
        a1c = math.sqrt((corner[0] - triangle.x1)**2 + (corner[1] - triangle.y1)**2)
        a3c = math.sqrt((corner[0] - triangle.x3)**2 + (corner[1] - triangle.y3)**2)
        s_13c = (a13 + a1c + a3c)/2
        area_13c = math.sqrt(s_13c * (s_13c - a13) * (s_13c - a1c) * (s_13c - a3c))

        sum_of_areas = area_12c + area_23c + area_13c
        list_of_sum_of_areas.append(sum_of_areas)
    return list_of_sum_of_areas

def calc_new_speeds(circle, triangle):
    """a fucntion to determine the x and y velocity of the ball after hitting a banked surface,
    using the assumptions that the tangential velocity will remain constant after impact ad the normal component will be reversed"""
    #find the magnitude of the initial speed
    mag_vi = math.sqrt(circle.x_vel**2 + circle.y_vel**2)
    #find the angle of the nitial speed
    theta1 = math.atan2(circle.y_vel, circle.x_vel)
    #the angle of the banked surface will be 45 degrees
    theta2 = math.pi / 4
    #find the relative angle of velocity relative to the banked sufrace
    phi = theta2 - theta1
    #break down the inital velocity components into normal and tangential to the surface
    v_it = mag_vi * math.cos(phi)
    v_in = mag_vi * math.sin(phi)
    #express the velocity post collision in normal and tangential components
    v_ft = v_it
    v_fn = -v_in
    #find the magnitues of the final velocity and break in down into x and y components
    mag_vf = math.sqrt(v_fn**2 + v_ft**2)

    #these values work for collisions on topleft and bottomright triangles

    #v_fx = -mag_vf * math.cos(theta2 + phi)
    #v_fy = -mag_vf * math.sin(theta2 + phi)

    #these values work for collisions on bottomleft and topright triangles
    if (circle.centerx > triangle.x3 and circle.centery < triangle.y3):
        print('bottom left')
        v_fx = mag_vf * math.cos(theta2 + phi)
        v_fy = mag_vf * math.sin(theta2 + phi)
    elif circle.centerx < triangle.x3 and circle.centery > triangle.y3:
        print('top right')
        v_fx = mag_vf * math.cos(theta2 + phi)
        v_fy = mag_vf * math.sin(theta2 + phi)
    elif circle.centerx < triangle.x3 and circle.centery < triangle.y3:
        print('botright')
        v_fx = -mag_vf * math.cos(theta2 + phi)
        v_fy = -mag_vf * math.sin(theta2 + phi)
    elif circle.centerx > triangle.x3 and circle.centery > triangle.y3:
        print('topleft')
        v_fx = -mag_vf * math.cos(theta2 + phi)
        v_fy = -mag_vf * math.sin(theta2 + phi)
    #equate the circles velocity components to these new values
    circle.x_vel = v_fx
    circle.y_vel = v_fy

def find_collision(triangle, circle):
    """determine if the ball has colided with the banked surface, we compare the area of the original triangle 
       with the sum of area of the three triangles made bwteen the point and the corners of the triangle"""
    #the logic for the collision test is explained further in https://www.jeffreythompson.org/collision-detection/tri-point.php
    #set a variable equal to the area of the original triangle
    area_of_triangle = find_area_of_triangle(triangle)
    #print( 'area of triangle = ', area_of_triangle)
    #call a function which find the sum of the three triangles made with the corners of the original triangle and the point
    list_of_sum_of_areas = sum_of_areas_between_circle_and_triangle(circle, triangle)
    #print('sum of areas between circle = ', sum_of_areas)
    #evaluate if the sum of areas is less than the original area, which indicates a collision
    for sum_of_areas in list_of_sum_of_areas:
        if sum_of_areas <= area_of_triangle*1.01:
            #print('hit')
            return True
        
def find_nearest_triangle(ball, triangles):
    smallest_distance = 99999
    closest_triangle = ' '
    for triangle in triangles:
        distance = math.sqrt((ball.centerx - triangle.x3)**2 + (ball.centery - triangle.y3)**2)
        if distance < smallest_distance:
            smallest_distance = distance
            closest_triangle = triangle
    return closest_triangle


    


"""
triangles = []
triangle1 = Triangle(0, 350, 350, 700, 0, 700, tri_colour, screen)
triangle2 = Triangle(350, 0, 700, 350, 700, 0,tri_colour, screen)
triangle3 = Triangle(350, 0, 0, 350, 0, 0, tri_colour, screen)
triangle4 = Triangle(350, 700, 700, 350, 700, 700, tri_colour, screen)
triangles.append(triangle1)
triangles.append(triangle2)
triangles.append(triangle3)
triangles.append(triangle4)

circle = Circle(200, 200, 25, screen, ball_colour)


while True:
    screen.fill(bg_colour)
    for triangle in triangles:
        triangle.draw_triangle()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #circle.cx, circle.cy = pygame.mouse.get_pos()
    circle.draw_circle()
    print(circle.corners)
    for triangle in triangles:
        if find_collision(triangle, circle):
            print(triangle.x3, triangle.y3)
            calc_new_speeds(circle, triangle)
    circle.update()
   

    pygame.display.flip()
    #sleep(0.01)"""
