import pygame
import pandas as pd
# variables
WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELO = 1
FRAMERATE=600


# Defining the classes
class Ball:
    RADIUS = 20

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def show(self, colour):
        global screen
        pygame.draw.circle(screen, colour, (self.x, self.y), self.RADIUS)

    def update(self):
        global fgcolour, bgcolour
        self.show(bgcolour)
        newx = self.x + self.vx
        newy = self.y + self.vy

        if newx < BORDER + self.RADIUS:
            self.vx = -self.vx
        elif newy < BORDER + self.RADIUS or newy > HEIGHT - BORDER - self.RADIUS:
            self.vy = -self.vy
        elif newx+self.RADIUS > WIDTH-Paddel.WIDTH and abs(newy-paddel.pp) < Paddel.HEIGHT//2:
            self.vx = -self.vx
        else:
            self.show(bgcolour)
            self.x = self.x + self.vx
            self.y = self.y + self.vy
            self.show(fgcolour)

        self.show(fgcolour)


class Paddel:
    WIDTH = 20
    HEIGHT = 200

    def __init__(self, pp):
        self.pp=pp

    def show(self, colour):
        global screen
        #pygame.draw.rect(screen, colour, pygame.Rect((BORDER, (HEIGHT//3)), (self.WIDTH, self.HEIGHT)))
        pygame.draw.rect(screen, colour, pygame.Rect((WIDTH - self.WIDTH, self.pp - self.HEIGHT // 2), (self.WIDTH, self.HEIGHT)))

    def update(self):
        self.show(pygame.Color("black"))
        self.pp = pygame.mouse.get_pos()[1]
        self.show(pygame.Color("white"))

        """newy = pygame.mouse.get_pos()[1]
        if newy-self.HEIGHT//2>BORDER \
            and newy+self.HEIGHT//2<HEIGHT-BORDER:
            self.show(bgcolour)
            self.y = newy
            self.show(fgcolour)"""


# Create object

ballplay = Ball(WIDTH - Ball.RADIUS-Paddel.WIDTH-10, HEIGHT // 2, -VELO, -VELO)
paddel = Paddel(HEIGHT//3)

# Draw the scenario
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bgcolour = pygame.Color("black")
fgcolour = pygame.Color("green")

pygame.draw.rect(screen, fgcolour, pygame.Rect((0, 0), (WIDTH, BORDER)))
pygame.draw.rect(screen, fgcolour, pygame.Rect(0, 0, BORDER, HEIGHT))
pygame.draw.rect(screen, fgcolour, pygame.Rect(0, HEIGHT - BORDER, WIDTH, BORDER))
ballplay.show(fgcolour)
paddel.show(fgcolour)
clock = pygame.time.Clock()

# sample = open("game.csv", "w")
# print("X, Y, VX, VY,Paddel.y", file=sample)

pong = pd.read_csv("game.csv")
pong = pong.drop_duplicates()

X_Train = pong.drop(columns="Paddel.y")
Y_Train = pong["Paddel.y"]

from sklearn.neighbors import KNeighborsRegressor

clf = KNeighborsRegressor(n_neighbors=3)
clf = clf.fit(X_Train,Y_Train)

df = pd.DataFrame(columns=["x", 'y', 'vx', 'vy'])


while True:

    e = pygame.event.poll()

    if e.type == pygame.QUIT:
        break
    clock.tick(FRAMERATE)
    pygame.display.flip()

    toPredict = df.append({'x': ballplay.x, 'y': ballplay.y, 'vx': ballplay.vx, 'vy': ballplay.vy}, ignore_index=True)
    desired_position = clf.predict(toPredict)

    paddel.update()
    ballplay.update()
    #print("{}, {}, {}, {}, {}".format(ballplay.x, ballplay.y, ballplay.vx, ballplay.vy, paddel.pp), file=sample)


pygame.quit()
