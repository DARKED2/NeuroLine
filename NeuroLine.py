import pygame
import math
from sklearn.linear_model import LinearRegression
import numpy as np


# Initialization Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

points = [(-40, -40), (0, 0), (40, 40)] #Coordinates of three points 

POINT_RADIUS = 7 #Point Radius 
line_thickness = 2 # Line Thickness
is_mouse_pressed_left = False

# Setting Window Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Creates a window with the specified dimensions
pygame.display.set_caption("NeuroLine") # sets the window title 

#Function to find the linear regression line
def linear_regression(points):
    Xs = []
    Ys = []
    #Fill our arrays with values from the points array
    for index in points:
        Xs.append(index[0])
        Ys.append(index[1])

    #Convert regular arrays Xs,Ys to numpy array
    Xs =np.array(Xs).reshape(-1, 1)
    Ys = np.array(Ys)

    model = LinearRegression() # Call the function from the Sklearn library

    #Fit the model to the data
    model.fit(Xs, Ys)
    
    w = model.coef_ # Get the value of w
    b = model.intercept_ # Get the value of b





   #----------------------------------------------------------------
   # My function I make to compute linear regression
    # w = -7.6
    # b = -3.6

    # cost = 0
    # for index in range(len(points)):
    #     nx,ny = points[index]
    #     cost += (w*nx + b - ny)**2


    # old_cost = 0
    
    # while abs(cost - old_cost) > 0.00001:

    #     dcost_w = 0
    #     dcost_b = 0

    #     #"find the derivative"
    #     for index in range(len(points)):
    #         nx, ny = points[index]
    #         dcost_w += 2*(w * nx + b - ny) * nx
    #         dcost_b += 2*(w * nx + b - ny)

    #     old_cost = cost

    #     b = b - dcost_b * 0.0001
    #     w = w - dcost_w * 0.0001

    #     cost = 0
    #     for index in range(len(points)):
    #         nx,ny = points[index]
    #         cost += (w * nx + b - ny)**2

    return w,b


# Function to draw the coordinate axes
def draw_axes():
    pygame.draw.line(screen,BLACK,(WIDTH // 2,0),(WIDTH // 2 , HEIGHT))
    pygame.draw.line(screen,BLACK,(0, HEIGHT // 2), (WIDTH, HEIGHT // 2))

# Function to draw the line
def draw_line(w,b):
    x1 = -400
    x2 = 400
    y1 = w[0] * x1 + b
    y2 = w[0] * x2 + b

    #Shift the line to the center of the screen
    x1 += WIDTH//2
    y1 = HEIGHT//2 -y1
    x2 += WIDTH//2
    y2 = HEIGHT //2 - y2
    pygame.draw.line(screen,RED,(x1,y1), (x2,y2),line_thickness)

#Function to draw points on the coordinate plane
def draw_points():
    for point in points:
        x,y = point

        # Shift the point to the center of the screen
        x += WIDTH //2
        y = HEIGHT // 2 - y
        pygame.draw.circle(screen,RED,(x,y),POINT_RADIUS)

#Function to check if a point is touched
def check_point_touch(x,y,):
    for index in range(len(points)):
        px,py = points[index]

        # Shift the point to the center of the screen
        px += WIDTH //2
        py = HEIGHT //2 - py
        
        distance = ((x -px)**2 + (y - py)**2)**0.5
        if distance <= POINT_RADIUS:
            
            return index
    return -1

#Function to shift the point to the center of the screen
def Shifted_point_to_center(x,y):
    xm = x - WIDTH //2
    ym = HEIGHT // 2 - y
    return xm,ym

#Main program loop
running = True
index = -1
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Close the window
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Close the window on Escape key press
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                is_mouse_pressed_left = True
                x, y = pygame.mouse.get_pos()
                index = check_point_touch(x, y)
                if index != -1:
                    print("Clicked on point:", index)

            if event.button == 3:  # Right mouse button click
                mouse_x, mouse_y = event.pos
                points.append(Shifted_point_to_center(mouse_x, mouse_y))

        elif event.type == pygame.MOUSEMOTION:  # Mouse movement
            if is_mouse_pressed_left and index != -1:
                mouse_x, mouse_y = event.pos
                points[index] = Shifted_point_to_center(mouse_x, mouse_y)  # Update point coordinates

        elif event.type == pygame.MOUSEBUTTONUP:
            is_mouse_pressed_left = False  # Reset left mouse button press flag

    # Update and draw graphics
    screen.fill(WHITE)
    draw_axes()
    draw_points()
    w, b = linear_regression(points)  # Perform linear regression
    draw_line(w, b)  # Draw the regression line
    pygame.display.flip()  # Update the display

pygame.quit()  # Quit Pygame