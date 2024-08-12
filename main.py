import pygame 
import math

pygame.init()

WIDTH = 500
HEIGHT = 500

PLAYER_SPEED = 5
PLAYER_ROT_SPEED = 5

FOV_CONST = 200

BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Sector:
    def __init__(self, point1, point2, color = "red"):
        self.point1 = point1
        self.point2 = point2
        self.color = color
    def translate(self, x: int, y: int):
        self.point1 = [self.point1[0] + x, self.point1[1] + y, self.point1[2]]
        self.point2 = [self.point2[0] + x, self.point2[1] + y, self.point2[2]]
    def rotate(self, angle):
        angle_rad = math.radians(angle)
        x1, y1, z1 = self.point1
        x2, y2, z2 = self.point2

        x1 -= WIDTH/2
        y1 -= HEIGHT/2
        x2 -= WIDTH/2
        y2 -= HEIGHT/2

        new_x1 = x1 * math.cos(angle_rad) - y1 * math.sin(angle_rad)
        new_y1 = (x1 * math.sin(angle_rad)) + (y1 * math.cos(angle_rad))
        new_x2 = (x2 * math.cos(angle_rad)) - (y2 * math.sin(angle_rad))
        new_y2 = (x2 * math.sin(angle_rad)) + (y2 * math.cos(angle_rad))

        new_x1 += WIDTH/2
        new_y1 += HEIGHT/2
        new_x2 += WIDTH/2
        new_y2 += HEIGHT/2

        self.point1 = [new_x1, new_y1, z1]
        self.point2 = [new_x2, new_y2, z2]
    def draw_top_down(self, screen):
        pygame.draw.line(screen, self.color, (self.point1[0], self.point1[1]), (self.point2[0], self.point2[1]), 5)

class Wall:
    def __init__(self, point1, point2, height, color = 'black'):
        self.bottom_point1 = point1
        self.bottom_point2 = point2

        top_point_z1 = point1[2] + height
        top_point_z2 = point2[2] + height

        self.top_point1 = [point1[0], point1[1], top_point_z1]
        self.top_point2 = [point2[0], point2[1], top_point_z2]

        self.top_sector = Sector(self.top_point1, self.top_point2, color)
        self.bottom_sector = Sector(self.bottom_point1, self.bottom_point2, color)

        self.color = color
    def translate(self, x, y):
        self.bottom_sector.translate(x, y)
        self.top_sector.translate(x, y)

        self.top_point1 = self.top_sector.point1
        self.top_point2 = self.top_sector.point2

        self.bottom_point1 = self.bottom_sector.point1
        self.bottom_point2 = self.bottom_sector.point2
    def rotate(self, angle):
        self.bottom_sector.rotate(angle)
        self.top_sector.rotate(angle)

        self.top_point1 = self.top_sector.point1
        self.top_point2 = self.top_sector.point2

        self.bottom_point1 = self.bottom_sector.point1
        self.bottom_point2 = self.bottom_sector.point2
    def draw(self, screen):
        # Turn the points to screen pos 
        screen_points = []
        try:    
            for point in [self.top_point1, self.bottom_point1, self.bottom_point2, self.top_point2]:
                point[2] = point[2] 

                screen_x = point[0] * FOV_CONST / point[1] + WIDTH/2
                screen_y = point[2] * FOV_CONST / point[1] + HEIGHT/2
                screen_points.append((screen_x, screen_y))
            pygame.draw.polygon(screen, self.color, screen_points)
        except:
            pass

    def draw_top_down(self, screen):
        self.top_sector.draw_top_down(screen)
        self.bottom_sector.draw_top_down(screen)

        
        


class Player:
    def __init__(self, position, facing):
        self.position = position
        self.facing = facing
    def draw_top_down(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), self.position, 10)


class Scene:
    def __init__(self, scene: list):
        self.scene = scene
    def translate(self, x: int, y: int):
        for sector in self.scene:
            sector.translate(x, y)
    def rotate(self, angle):
        for sector in self.scene:
            sector.rotate(angle)
    def draw(self, screen):
        for sector in self.scene:
            sector.draw(screen)
    def draw_top_down(self, screen):
        for sector in self.scene:
            sector.draw_top_down(screen)

def handle_inputs(keys, scene):
    
    if keys[pygame.K_w]:
        scene.translate(0,PLAYER_SPEED)
    if keys[pygame.K_s]:
        scene.translate(0, -PLAYER_SPEED)
    if keys[pygame.K_a]:
        scene.translate(PLAYER_SPEED, 0)
    if keys[pygame.K_d]:
        scene.translate(-PLAYER_SPEED, 0)
    if keys[pygame.K_COMMA]:
        scene.rotate(-PLAYER_ROT_SPEED)
    if keys[pygame.K_PERIOD]:
        scene.rotate(PLAYER_ROT_SPEED) 



room = [
    Wall([10, 10, 0], [30, 10, 0], 10, (83, 28, 179)),
    Wall([10, 10, 0], [10, 30, 0], 10, (148, 75, 187)),
    Wall([10, 30, 0], [30, 30, 0], 10, (170, 123, 195)),
    Wall([30, 10, 0], [30, 30, 0], 10, (219, 168, 172)),
]

scene = Scene(room)

player = Player((WIDTH/2, HEIGHT/2), (240,240))


clock = pygame.time.Clock()

while True:
    screen.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        

    
    keys = pygame.key.get_pressed()
    handle_inputs(keys, scene)
    scene.draw(screen)
    

    clock.tick(30)
    pygame.display.update()